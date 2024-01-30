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

1. **Create OAuth 2.0 Client ID**:
   - Navigate to "APIs & Services > Credentials".
   - Click "Create Credentials" and select "OAuth client ID".
   - Choose "Desktop app" as the Application type, provide a name, and create.

2. **Download OAuth Client Configuration**:
   - After creating the OAuth client ID, download the client configuration JSON file.
   - This file contains your client ID and secret, which are necessary for the OAuth flow.
#### Note:
- The script uses the `token.pickle` file to store access tokens and refresh tokens. Once authenticated, you won't need to repeat the process unless the token is revoked or expired.


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
pip install google-analytics-data google-cloud-bigquery google-auth google-auth-oauthlib google-auth-httplib2
```

### Step 6: Authentication

- **Run the Script**:
  - Execute your Python script.
  - It will prompt you to open a URL for authentication.
  - After authentication, you'll receive a verification code.
  - Copy and paste this code back into the script.
 
Understood, I'll insert a step before the final verification, explaining how to run the script with the desired flags (`--yesterday` or `--initial_fetch`). This step will guide users on how to execute the script properly after setting up the configuration and authentication.

---

## Installation and Setup

[Previous sections remain the same]

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


### Step 8: Final Execution

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

Encourage other developers to contribute to your project. Provide clear guidelines on how they can contribute.

```markdown
Contributions to this project are welcome! Here's how you can help:

- **Reporting Issues**: Report issues or bugs by opening a new issue in the GitHub repository.
- **Feature Requests**: If you have ideas for new features or improvements, feel free to create an issue describing your suggestion.
- **Submitting Pull Requests**: You can contribute directly to the codebase. Please ensure your code adheres to the project's coding standards and include tests for new features.
```


## Contact
For help, feedback, or discussions about potential features, please feel free to connect with me on [Linkedin](https://www.linkedin.com/in/ali-iz/).

