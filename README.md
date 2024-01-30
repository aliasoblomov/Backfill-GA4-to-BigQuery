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

### Step 2: Creating a Service Account

1. **Access Google Cloud Console**: Visit the [Google Cloud Console](https://console.cloud.google.com/).

2. **Select/Create a Project**: Choose an existing project or create a new one.

3. **Create a Service Account**:
   - Navigate to "IAM & Admin > Service Accounts".
   - Click "Create Service Account", enter a name, description, and click "Create".
   - Grant necessary roles to the service account (e.g., BigQuery Admin).

4. **Generate a Service Account Key**:
   - Click on the created service account to manage it.
   - Go to the "Keys" tab and click "Add Key", then "Create new key".
   - Choose "JSON" as the key type and click "Create".
   - A JSON key file will be downloaded. Store it securely.
  

### Step 3: Setting Up OAuth for Desktop App

To set up OAuth for a desktop application, you need to create an OAuth client ID in Google Cloud Console. Before creating an OAuth client ID, make sure to configure your consent screen if you don't have one already.

#### Configure the Consent Screen:

1. **Access Consent Screen Configuration**:
   - In the Google Cloud Console, navigate to "APIs & Services > OAuth consent screen".
   - Select the external user type.
   
2. **Fill in Consent Screen Details**:
   - Provide the necessary information, such as the app name, user support email, and developer contact information.
   -  add your email (and others, if needed) in the "Test users" section.

4. **Publish the App**:
   - Once all necessary information is provided, save and publish your consent screen.

#### Create OAuth 2.0 Client ID:

1. **Navigate to Credentials**:
   - Go to "APIs & Services > Credentials".

2. **Create OAuth Client ID**:
   - Click "Create Credentials" and select "OAuth client ID".
   - Choose "Desktop app" as the Application type.
   - Provide a name for the client ID and click "Create".

3. **Download Client Configuration**:
   - After the OAuth client ID is created, download the client configuration JSON file.
   - This file contains your client ID and secret, which are essential for the OAuth flow.

#### Note:

- The script uses a `token.pickle` file to store access tokens and refresh tokens. Once authenticated, you won't need to repeat the authentication process unless the token is revoked or expired.
- Ensure that the JSON file is stored securely and referenced correctly in your project.


### Step 4: Configuration File
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

### Step 5: Installation of Dependencies
Install necessary Python packages:
```bash
pip install google-analytics-data
pip install google-cloud-bigquery
pip install google-auth
pip install google-auth-oauthlib
pip install google-auth-httplib2
```

### Step 6: Authentication

- **Run the Script**:
  - Execute your Python script.
  - It will prompt you to open a URL for authentication.
  - After authentication, you'll receive a verification code.
  - Copy and paste this code back into the script.
 

### Step 7: Running the Script

After configuring the `config.json` file and ensuring authentication setup is complete, it's time to run the script with the desired flags.

- **Execute the Script with Flags**:
  - Use the `%run` command followed by the script name and the desired flag.
  - For fetching data from yesterday, use:
    ```bash
    %run backfill-ga4.py --yesterday
    ```
  - For fetching data from the initial fetch date specified in your `config.json`, use:
    ```bash
    %run backfill-ga4.py --initial_fetch
    ```
  - This will start the data retrieval process based on the specified date range.


### Step 8: QA

- **Check for Successful Setup**:
  - Upon successful completion of the script, it should indicate that the authentication process is complete and data fetching has started.
  - Now, you should be able to see the new tables in your Google Analytics BigQuery dataset (`DATASET_ID` specified in your `config.json`).
  - Additionally, the `output.csv` file in your project directory should contain the fetched data.
  - If the tables are visible and the CSV file has data, everything is set up correctly.
 

## Customization

Your project can be customized to fetch different metrics and dimensions based on your specific needs. Use the [Google Analytics Data API schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) to understand the available metrics and dimensions. You can then modify the script to query different sets of data from your Google Analytics account.

- **Tailor Metrics and Dimensions**: In the script, identify the sections where API requests are constructed and modify the `metrics` and `dimensions` according to your requirements.
- **Consult API Schema**: The API schema documentation provides a comprehensive list of all available metrics and dimensions, along with their descriptions and usage.


## Contributing

Contributions to this project are welcome! Here's how you can help:

- **Reporting Issues**: Report issues or bugs by opening a new issue in the GitHub repository.
- **Feature Requests**: If you have ideas for new features or improvements, feel free to create an issue describing your suggestion.
- **Submitting Pull Requests**: You can contribute directly to the codebase. Please ensure your code adheres to the project's coding standards and include tests for new features.


## Contact
For help, feedback, or discussions about potential features, please feel free to connect with me on [Linkedin](https://www.linkedin.com/in/ali-iz/).

