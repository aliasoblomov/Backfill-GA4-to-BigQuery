import csv
import argparse
import datetime
import sys
import json
import os
import pickle
from google.analytics.data_v1beta import BetaAnalyticsDataClient, OrderBy
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from google_auth_oauthlib.flow import Flow

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

#  function to validate and ensure FETCH_TO_DATE is correct
def get_valid_end_date(end_date_str):
    try:
        valid_end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        valid_end_date = datetime.date.today()
    return valid_end_date

# Validate or default FETCH_TO_DATE from the config
valid_end_date = get_valid_end_date(config.get('FETCH_TO_DATE'))
FETCH_TO_DATE = valid_end_date.strftime('%Y-%m-%d')

# Function to check if an event exists in BigQuery
def exists_in_bigquery(event_name, event_date, event_count, channel_group, dataset_id, bq_client):
    year = event_date[:4]
    month = event_date[4:6]
    table_id = f'{TABLE_PREFIX}{year}{month}01'
    table_ref = bq_client.dataset(dataset_id).table(table_id)

    try:
        bq_client.get_table(table_ref)
    except NotFound:
        return False


    params = [
        bigquery.ScalarQueryParameter('event_name', 'STRING', event_name),
        bigquery.ScalarQueryParameter('event_date', 'INTEGER', event_date),
        bigquery.ScalarQueryParameter('event_count', 'INTEGER', event_count),
        bigquery.ScalarQueryParameter('channel_group', 'STRING', channel_group)
    ]

    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = params

    result = bq_client.query(query, job_config=job_config).result()
    count = list(result)[0][0]

    if count > 0:
        print(f"..record already exists in BigQuery ({count})", flush=True)

    return count > 0

def get_table_ref(year, month):
    table_id = f'{TABLE_PREFIX}{year}{month}01'
    return bq_client.dataset(DATASET_ID).table(table_id)

# Configuration parameters
CLIENT_SECRET_FILE = config['CLIENT_SECRET_FILE']
SCOPES = config['SCOPES']
TABLE_PREFIX = config['TABLE_PREFIX']
PROPERTY_ID = config['PROPERTY_ID']
DATASET_ID = config['DATASET_ID']
INITIAL_FETCH_FROM_DATE = config['INITIAL_FETCH_FROM_DATE']
SERVICE_ACCOUNT_FILE = config['SERVICE_ACCOUNT_FILE']
PARTITION_BY = config.get('PARTITION_BY', 'Event_Date')  # Default to Event_Date
CLUSTER_BY = config.get('CLUSTER_BY', 'Event_Name')
FETCH_TO_DATE = config.get('FETCH_TO_DATE', datetime.date.today().strftime('%Y-%m-%d')) 


# Command line arguments for date range
parser = argparse.ArgumentParser(description='Fetch data based on date range.')
parser.add_argument('--yesterday', action='store_true', help='Fetch data from yesterday only.')
parser.add_argument('--initial_fetch', action='store_true', help='Fetch data from a wide date range.')
args = parser.parse_args()

# Determine date range
start_date = None
end_date = None
if args.yesterday:
    date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = end_date = date.strftime('%Y-%m-%d')
elif args.initial_fetch:
    confirmation = input("Using the initial_fetch might result in duplicated records. Do you want to proceed? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        start_date = INITIAL_FETCH_FROM_DATE
        end_date = FETCH_TO_DATE  
    else:
        print("Exiting script due to user cancellation.", flush=True)
        sys.exit()
else:
    print("No valid date range argument provided. Exiting script.", flush=True)
    sys.exit()
print(f"Starting fetching data from {start_date} to {valid_end_date.strftime('%Y-%m-%d')}.", flush=True)

# Authenticate with service account for BigQuery
creds1 = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/analytics.readonly', 'https://www.googleapis.com/auth/bigquery']
)
bq_client = bigquery.Client(credentials=creds1, project=creds1.project_id)

# Authenticate for Analytics Data API
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
else:
    # Create the flow using the client secrets file
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, 
        scopes=SCOPES,
        redirect_uri='http://localhost:8080/'
    )

    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')

    print('Please go to this URL and finish the authentication: ', auth_url)
    code = input('Enter the authorization code: ')
    flow.fetch_token(code=code)

    creds = flow.credentials

    # Save the credentials for future use
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

print("Authentication successful!")

client = BetaAnalyticsDataClient(credentials=creds)

# Function to run report with pagination
def run_report_with_pagination(client, request):
    all_rows = []
    offset = 0  # Initialize offset
    limit = 10000  # Set limit (maximum rows per request)

    while True:
        # Apply offset and limit to request
        request.offset = offset
        request.limit = limit

        response = client.run_report(request)
        all_rows.extend(response.rows)

        # Check if there are more rows to fetch
        if len(response.rows) == limit:
            offset += limit  # Increase offset for the next iteration
        else:
            break  # No more rows left, exit loop

    return all_rows

# Requests for active users and events
request_active_users = RunReportRequest(
    property=f'properties/{PROPERTY_ID}',
    date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    dimensions=[
        Dimension(name='date'),
        Dimension(name='sessionDefaultChannelGroup')
    ],
    metrics=[Metric(name='sessions')],
    order_bys=[OrderBy({"dimension": {"dimension_name": "date"}})]
)

active_users = run_report_with_pagination(client, request_active_users)

request_events = RunReportRequest(
    property=f'properties/{PROPERTY_ID}',
    date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    dimensions=[Dimension(name='eventName'), Dimension(name='date'), Dimension(name='isConversionEvent'), Dimension(name='sessionDefaultChannelGroup')],
    metrics=[Metric(name='eventCount')]
)

all_events = run_report_with_pagination(client, request_events)

# Process and write data to CSV
rows_by_month = {}

with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Event Name', 'Event Date', 'Event Count', 'Is Conversion', 'Channel', 'Event_Type'])

    # Processing active users data
    for row in active_users:
        event_name = "ct_active_users"
        is_conversion = None
        event_date = row.dimension_values[0].value
        channel_group = row.dimension_values[1].value
        event_count = row.metric_values[0].value
        event_type = "Traffic"

        csv_writer.writerow([event_name, event_date, event_count, is_conversion, channel_group, event_type])

        # Check for existing records in BigQuery
        if not (args.yesterday and exists_in_bigquery(event_name, event_date, event_count, channel_group, DATASET_ID, bq_client)):
            year, month = event_date[:4], event_date[4:6]
            key = (year, month)
            rows_by_month.setdefault(key, []).append({
                "Event_Name": event_name,
                "Event_Date": event_date,
                "Event_Count": event_count,
                "Is_Conversion": is_conversion,
                "Channel": channel_group,
                "Event_Type": event_type
            })

    # Sort and process events data
    sorted_events = sorted(all_events, key=lambda x: x.dimension_values[1].value)
    for row in sorted_events:
        event_name = row.dimension_values[0].value
        event_date = row.dimension_values[1].value
        is_conversion = row.dimension_values[2].value

        if is_conversion == "(not set)":
            is_conversion = ""

        channel_group = row.dimension_values[3].value
        event_count = row.metric_values[0].value

        is_conversion = bool(is_conversion)
        event_type = "Conversion" if is_conversion else "Event"

        csv_writer.writerow([event_name, event_date, event_count, is_conversion, channel_group, event_type])

        # Check for existing records in BigQuery
        if not (args.yesterday and exists_in_bigquery(event_name, event_date, event_count, channel_group, DATASET_ID, bq_client)):
            year, month = event_date[:4], event_date[4:6]
            key = (year, month)
            rows_by_month.setdefault(key, []).append({
                "Event_Name": event_name,
                "Event_Date": event_date,
                "Event_Count": event_count,
                "Is_Conversion": is_conversion,
                "Channel": channel_group,
                "Event_Type": event_type
            })

print("Data saved to output.csv!", flush=True)

def create_or_update_table_with_partition_and_cluster(dataset_id, simple_table_id, schema, partition_by=None, cluster_by=None):
    full_table_id = f"{bq_client.project}.{dataset_id}.{simple_table_id}"  # Correctly construct the full table ID
    table = bigquery.Table(full_table_id, schema=schema)
    
    if partition_by:
        table.time_partitioning = bigquery.TimePartitioning(field=partition_by)
        
    if cluster_by:
        table.clustering_fields = [cluster_by]
    
    try:
        # Attempt to create the table, or if it exists, confirm it's updated
        created_table = bq_client.create_table(table, exists_ok=True)
        print(f"Table {created_table.full_table_id} created or confirmed existing with specified settings.")
    except Exception as e:
        print(f"Error creating or confirming table: {e}")

TABLE_PREFIX = config.get('TABLE_PREFIX')  # Handle potential absence of key
DATASET_ID = config['DATASET_ID']

schema = [
    bigquery.SchemaField("Event_Name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Event_Date", "DATE", mode="NULLABLE"),  
    bigquery.SchemaField("Event_Count", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Is_Conversion", "BOOLEAN", mode="NULLABLE"),
    bigquery.SchemaField("Channel", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Event_Type", "STRING", mode="NULLABLE"),
]

def format_event_date(event_date):
    return f"{event_date[:4]}-{event_date[4:6]}-{event_date[6:]}"

table_id = f"{bq_client.project}.{DATASET_ID}.{TABLE_PREFIX}"

try:
    bq_client.get_table(table_id)
    print(f"Table {table_id} already exists.")
except NotFound:
    # If table does not exist, create it
    print(f"Table {table_id} not found. Creating table...")
    table = bigquery.Table(table_id, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        field=config["PARTITION_BY"],
        type_=bigquery.TimePartitioningType.DAY
    )
    if "CLUSTER_BY" in config and config["CLUSTER_BY"]:
        table.clustering_fields = [config["CLUSTER_BY"]]
    bq_client.create_table(table)
    print(f"Created table {table_id}")

all_rows_to_insert = []
for _, month_data in rows_by_month.items():
    for row in month_data:
        # Format the 'Event_Date' to match BigQuery DATE format 'YYYY-MM-DD'
        if 'Event_Date' in row:
            row['Event_Date'] = format_event_date(row['Event_Date'])
        all_rows_to_insert.append(row)

# Now, insert all rows into the single table
if all_rows_to_insert:
    errors = bq_client.insert_rows_json(table_id, all_rows_to_insert)  # Use insert_rows_json for better performance with dicts
    if errors:
        print("Errors:", errors, flush=True)
    else:
        print(f"Data saved to BigQuery!", flush=True)
else:
    print("No data to insert.")
