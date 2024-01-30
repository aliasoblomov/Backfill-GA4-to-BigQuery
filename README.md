# Backfill-GA4-to-BigQuery
Backfill-GA4-to-BigQuery" repository offers a solution for users to backfill their GA4 data into BigQuery. This is useful for those who need historical data from the start of their GA4 property, as GA4 data is typically only available in BigQuery after linking the two services. Our solution provides a complete backfill of data to BigQuery. It uses OAuth 2.0 credentials for desktop applications, making authentication easier and well-suited for IDEs like Google Colab.

## Features
- **OAuth 2.0 Authentication**: Simplified authentication using OAuth 2.0 credentials for desktop apps, with an easy-to-follow local host URL verification method.
- **Service Account Integration**: Secure connection to Google Cloud services via service accounts.
- **Comprehensive Data Extraction**: Fetch GA4 data from the initial setup date.
- **Customizable Configuration**: `config.json` file to tailor the data extraction process.
- **BigQuery Integration**: Efficiently processes and saves data into BigQuery with proper schema management.

## Prerequisites
- Google Cloud account with billing enabled.
- Access to Google Analytics 4 and Google BigQuery.
- Python environment (Python 3.x recommended).

## Setup and Installation

### Step 1: Create New Dataset and Activate Analytics API
- Go to [Google Cloud Console](https://console.cloud.google.com/apis/api/analyticsdata.googleapis.com/metrics) to create a new dataset and activate the Analytics API.

### Step 2: OAuth Credential and Service Account Creation
- Set up OAuth credentials for a desktop application and create a service account in Google Cloud Console. Download the JSON key file for the service account.

### Step 3: Configuration File
Fill out and save a `config.json` file with your specific parameters. Example:
```json
{
  "CLIENT_SECRET_FILE": "<Path to your client secret file>",
  "SERVICE_ACCOUNT_FILE": "<Path to your service account JSON file>",
  "SCOPES": ["https://www.googleapis.com/auth/analytics.readonly"],
  "TABLE_PREFIX": "<Prefix for the BigQuery tables>",
  "PROPERTY_ID": "<Google Analytics Property ID>",
  "DATASET_ID": "<BigQuery Dataset ID>",
  "INITIAL_FETCH_FROM_DATE": "YYYY-MM-DD"
}
```

### Step 4: Installation of Dependencies
Install necessary Python packages:
```bash
pip install google-analytics-data google-cloud-bigquery google-auth google-auth-oauthlib google-auth-httplib2
```

### Step 5: Script Setup
Save the provided main Python script to your project directory.

## Usage
Run the script with the desired flags (`--yesterday` or `--initial_fetch`). The script includes two authentication steps:
1. **Service Account Authentication for BigQuery**: This uses the service account JSON file for BigQuery operations.
2. **OAuth 2.0 Authentication for Analytics Data API**:
   - The script creates a flow from the client secrets file, generating an authorization URL.
   - Navigate to this URL, complete the authentication, and receive a verification code.
   - Enter this code back in the script to authenticate and create a token file for future use.

This authentication approach is especially advantageous for environments like Google Colab, where traditional authentication methods may be cumbersome.

## Contributing
Contributions are welcome. Please fork the repository and submit a pull request with your proposed changes.


## Contact
For support or queries, contact [Your Contact Information].

