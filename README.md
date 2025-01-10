# Backfill-GA4-to-BigQuery
Backfill-GA4-to-BigQuery" repository offers a solution for users to backfill their GA4 data into BigQuery. This is useful for those who need historical data from the start of their GA4 property, as GA4 data is typically only available in BigQuery after linking the two services. my solution provides a Game-Changer backfill of data to BigQuery. It uses OAuth 2.0 credentials for desktop applications, making authentication easier and well-suited for IDEs like Google Colab.

## What's New

I've added a **notebook version** of the code for working with GA4 data using Python and BigQuery! 

- If you prefer **straightforward, ready-to-use scripts** for creating GA4-like tables with minimal effort, the notebook provides a streamlined approach for quick setup. 
- For those looking to **customize the dimensions, metrics, or data handling processes**, the original main code remains your go-to option for flexibility and control.



## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup and Installation](#setup-and-installation)
   - [Step 1: Create New Dataset and Activate Analytics API](#step-1-create-new-dataset-and-activate-analytics-api)
   - [Step 2: Creating a Service Account](#step-2-creating-a-service-account)
   - [Step 3: Setting Up OAuth for Desktop App](#step-3-setting-up-oauth-for-desktop-app)
   - [Step 4: Configuration File](#step-4-configuration-file)
   - [Step 5: Installation of Dependencies](#step-5-installation-of-dependencies)
   - [Step 6: Running the Script](#step-6-running-the-script)
   - [Step 7: Authentication](#step-7-authentication)
   - [Step 8: QA](#step-8-qa)
4. [Using the Pre-Built Notebook for GA4 Reports](#using-the-pre-built-notebook-for-ga4-reports)
5. [Troubleshooting](#troubleshooting)
6. [Customization](#customization)
7. [Contributing](#contributing)
8. [Contact](#contact)



## Features

- **OAuth 2.0 Authentication**: Simplifies authentication with OAuth 2.0 credentials, ideal for desktop apps and environments like Google Colab.

- **Service Account Integration**: Securely connects to Google Cloud services using service accounts for enhanced security.

- **Data Extraction from GA4**: Fetches comprehensive GA4 data from a specified start date, ideal for historical data backfilling.

- **Customizable Configuration**: Offers a `config.json` file for user-specific settings like table prefixes and property IDs.

- **BigQuery Integration**: Efficiently processes and stores data in BigQuery with proper schema management.

- **Export Functionality**: Enables exporting GA4 data to CSV format for external use.

- **Duplicate Check**: Incorporates mechanisms to avoid duplicate data entries in BigQuery.

- **Flexible Data Retrieval**: Allows data fetching from a specific date or the previous day.

- **Robust Error Handling**: Includes effective error handling and logging for smooth operation.
  
- **Partitioning and clustering**: Dynamic partitioning and clustering for optimized query performance and cost management.

- **Configurable End Date Range**: precise control over the data retrieval period, making it easier to manage data quotas and perform historical data analysis within a specific timeframe.



## Prerequisites
- Google Cloud account with billing enabled.
- Access to Google Analytics 4 and Google BigQuery.
- Python environment (Python 3.x recommended).

## Setup and Installation

### Step 1: Create a New Project and Activate Analytics API
- Go to [Google Cloud Console](https://console.cloud.google.com/apis/api/analyticsdata.googleapis.com/metrics) to activate the Analytics API in your selected project.

### Step 2: Creating a Service Account

1. **Access Google Cloud Console**: Visit the [Google Cloud Console](https://console.cloud.google.com/).

2. **Create a Service Account**:
   - Navigate to "IAM & Admin > Service Accounts".
   - Click "Create Service Account", enter a name, description, and click "Create".
   - Grant necessary roles to the service account (e.g., Owner or BigQuery Admin + BigQuery Job User).

3. **Generate a Service Account Key**:
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
Fill out and save a `config.json` file with your specific parameters. 
Example:
```json
{
"CLIENT_SECRET_FILE": "<Path to your client secret file>",
"SERVICE_ACCOUNT_FILE": "<Path to your service account JSON file>",
"SCOPES": ["https://www.googleapis.com/auth/analytics.readonly"],
"PROPERTY_ID": "<Google Analytics Property ID>",
"INITIAL_FETCH_FROM_DATE": "2022-01-01",
"FETCH_TO_DATE": "today",
"DATASET_ID": "<BigQuery Dataset ID>",
"TABLE_PREFIX": "_backfill_GA4",
"PARTITION_BY": "Event_Date",
"CLUSTER_BY": "Event_Name"
}
```
- **Client Secret and Service Account File**: Replace the placeholders with the actual paths to your OAuth client secret and service account JSON files.

- **Property ID and Dataset ID**: Insert your Google Analytics Property ID and the BigQuery Dataset ID where data will be stored.

- **Initial Fetch Date**: Set the initial date from which to fetch historical data in `YYYY-MM-DD` format.

- **FETCH_TO_DATE**: Specify the end date for data fetching. Defaults to today's date. Format: `YYYY-MM-DD`.

- **Table Prefix**: Specify the prefix for your BigQuery tables. If the specified prefix does not exist, the script will create tables with this prefix in BigQuery.

- **PARTITION_BY**: Specifies the column for table partitioning. Default is Event_Date, which is highly recommended for optimal data management.
  
- **CLUSTER_BY**: Specifies the column(s) for table clustering. Default is Event_Name, aligning with common querying patterns. While this choice is optimal for many use cases, you may customize this field.

Install necessary Python packages:
```bash
!pip install google-analytics-data==0.18.4
!pip install google-cloud-bigquery
!pip install google-auth==2.27.0
!pip install google-auth-oauthlib
!pip install google-auth-httplib2
```

### Step 6: Running the Script

After configuring the `config.json` file and saving the source code with the same name `backfill-ga4.py` , it's time to run the script with the desired flags.

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
  - This will start the authentication flow 
    
### Step 7: Authentication

- **Run the Script**:
  - Execute your Python script.
  - It will prompt you to open a URL for authentication.
  - Ensure that you choose a Google account that has the necessary access to selected property.
  - If you don't verify your app in the first step, select "Go to 'YourPublishedAPP'(unsafe)" to access the authentication code on localhost.
  - Your code can be found as a part of the URL between "code=" and the next ampersand. (Screenshot attached)
    [![Ga4-bigquery-Script Authentication.png](https://i.postimg.cc/5N2T2Hkj/authentication-image.png)](https://postimg.cc/6TFYHQKN)
  - Copy and paste this code back into the script.
  - Now data retrieval process based on the specified date range should be completed. It is important that a table, that has been exported, is 
    visible in both Bigquery table and CSV downloadable file.

### Step 8: QA

- **Check for Successful Setup**:
  - Upon successful completion of the script, it should indicate that the authentication process is complete and data fetching has started.
  - Now, you should be able to see the new tables in your Google Analytics BigQuery dataset (`DATASET_ID` specified in your `config.json`).
  - Additionally, the `output.csv` file in your project directory should contain the fetched data.
  - If the tables are visible and the CSV file has data, everything is set up correctly.
    

## Using the Pre-Built Notebook for GA4 Reports

This repository now includes a **custom notebook** for exporting **13 of the most useful GA4 reports** into BigQuery and CSV format. This notebook simplifies the process, eliminating the need to dive into the source code. Follow the steps below to configure and run the notebook. Here is a clear breakdown of the tables that will be exported after running the notebook :


| **Table Name**                   | **Dimensions**                              | **Metrics**                                                                                     |
|-----------------------------------|---------------------------------------------|-------------------------------------------------------------------------------------------------|
| `ga4_transaction_items`          | `transactionId`, `itemName`, `date`         | `itemPurchaseQuantity`, `itemRevenue`                                                         |
| `ga4_data_session_channel_group` | `date`, `sessionDefaultChannelGroup`        | `sessions`, `totalUsers`, `newUsers`, `ecommercePurchases`, `purchaseRevenue`                  |
| `ga4_data_session_source_campaign_medium` | `date`, `sessionSource`, `sessionCampaignName`, `sessionMedium` | `sessions`, `totalUsers`, `newUsers`, `ecommercePurchases`, `purchaseRevenue` |
| `ga4_data_country_language_city` | `date`, `country`, `language`, `city`       | `sessions`, `screenPageViews`, `totalUsers`, `newUsers`, `ecommercePurchases`, `purchaseRevenue` |
| `ga4_data_item_name`             | `date`, `itemName`                          | `itemPurchaseQuantity`, `itemRevenue`                                                         |
| `ga4_data_browser_os_device`     | `date`, `browser`, `operatingSystem`, `deviceCategory` | `sessions`, `screenPageViews`, `totalUsers`, `newUsers`, `ecommercePurchases`, `purchaseRevenue` |
| `ga4_data_first_user_source_medium` | `date`, `firstUserMedium`, `firstUserSource`, `firstUserCampaignName` | `totalUsers`, `newUsers`, `ecommercePurchases`, `purchaseRevenue`                             |
| `ga4_data_first_user_channel_group` | `date`, `firstUserDefaultChannelGroup`     | `totalUsers`, `newUsers`, `ecommercePurchases`, `purchaseRevenue`                             |
| `ga4_ads_data`                   | `date`, `sessionSource`, `sessionMedium`, `sessionCampaignName` | `ecommercePurchases`, `averagePurchaseRevenue`, `purchaseRevenue`, `advertiserAdClicks`, `advertiserAdCost`, `advertiserAdCostPerClick`, `returnOnAdSpend` |
| `ga4_all_metrics_data`           | `date`                                      | `sessions`, `totalUsers`, `newUsers`, `ecommercePurchases`, `purchaseRevenue`, `screenPageViews`, `eventCount`, `averageSessionDuration`, `engagedSessions`, `engagementRate` |
| `ga4_event_metrics_data`         | `date`, `eventName`                         | `eventCount`, `eventCountPerUser`, `eventValue`                                               |
| `ga4_page_location_data`     | `date`, `pageLocation`                      | `totalUsers`, `ecommercePurchases`, `purchaseRevenue`, `screenPageViews`, `eventCount`, `engagementRate` |
| `ga4_landing_page_data`      | `date`, `landingPage`                       | `totalUsers`, `ecommercePurchases`, `purchaseRevenue`, `sessions`, `eventCount`, `engagementRate` |



### Steps to Use the Notebook

1. **Initial Steps**:
   The first three steps (creating a dataset, activating the Analytics API, and setting up OAuth) remain the same as detailed in the [Setup and Installation](#setup-and-installation) section.

2. **Prepare the Configuration File (`config.json`)**:
   Use the following template for the `config.json` file:
   ```json
   {
      "CLIENT_SECRET_FILE": "/path/to/your/client_secret.json",
      "SERVICE_ACCOUNT_FILE": "/path/to/your/service_account.json",
      "PROPERTY_ID": "<Your GA4 Property ID>",
      "INITIAL_FETCH_FROM_DATE": "YYYY-MM-DD",
      "FETCH_TO_DATE": "today",
      "DATASET_ID": "<Your BigQuery Dataset ID>",
      "SCOPES": ["https://www.googleapis.com/auth/analytics.readonly", "https://www.googleapis.com/auth/bigquery"]
   }
   ```
   Replace placeholders with your project-specific details.

3. **Run the Notebook**:
   - Upload the `config.json` file to the notebook directory.
   - Open and execute the cells in the notebook sequentially.
   - During execution, you will be prompted to authorize access. Follow the instructions to complete the OAuth flow.
   - Once authorized, the script will fetch the data and save it to BigQuery and a downloadable CSV.
 

## Troubleshooting

### AttributeError on Script Execution

**Issue:** Encountering an `AttributeError` related to `credentials.universe_domain` when running the script.

**Solution:** This is likely due to version mismatches in `google-auth` and `google-analytics-data` libraries. Resolve it by upgrading both libraries:

```shell
pip install --upgrade google-analytics-data google-auth
```

Run this command in your terminal or command prompt to ensure you're using compatible versions, which should fix the issue.


## Customization

Your project can be customized to fetch different metrics and dimensions based on your specific needs. Use the [Google Analytics Data API schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) to understand the available metrics and dimensions. You can then modify the script to query different sets of data from your Google Analytics account.

- **Tailor Metrics and Dimensions**: In the script, identify the sections where API requests are constructed and modify the `metrics` and `dimensions` according to your requirements.
- **Consult API Schema**: The API schema documentation provides a comprehensive list of all available metrics and dimensions, along with their descriptions and usage.


## Contributing

Contributions to this project are welcome! Here's how you can help:

- **Reporting Issues**: Report issues or bugs by opening a new issue in the GitHub repository.
- **Feature Requests**: If you have ideas for new features or improvements, feel free to create an issue describing your suggestion.
- **Submitting Pull Requests**: You can contribute directly to the codebase. Please ensure your code adheres to the project's coding standards and include tests for new features.


