# Utility to Export Control Room Audit Logs by Date Range

This utility allows users to export audit logs within a specified date range efficiently. The logs are fetched in batches of 400 records using an offset mechanism and exported to a CSV file. The process continues until all logs within the date range are retrieved.

## Key Features

1. **Batch Processing**
   - Fetches logs in chunks of 400 records to optimize performance.

2. **CSV Export:**
   - Logs are exported in a structured CSV format.

2. **Incremental Fetching**
   - Uses an offset to retrieve the next batch and appends it to the existing CSV file.

2. **Logging Mechanism**
   - Maintains a log file to track progress and errors.

2. **Supports Any Control Room**
   - The utility can fetch logs from any Control Room by providing the appropriate Control Room details as input.

## Pre-requisites

This utility(A360 Bot) has a dependent Python script (FetchAuditLogsV2.py) that requires the following libraries:

   - import json
   - import logging
   - import requests
   - import re

Before using this utility, ensure that the following requirements are met:

**1. Python Installation**
   - Install an appropriate version of **Python** on the system where you plan to execute the script.
   - Supported versions: **Python 2.x and 3.x**
   - Ensure the **PATH** environment variable includes the Python installation directory.
   - To verify the installation, run `python` in the command prompt. If the Python version is displayed, the environment variable is correctly set.


**2. Required Python Modules**
The following modules are needed for this script:
   - json (Built-in)
   - inspect (Built-in)
   - logging (Built-in)
   - requests (External)

To install the external module, run
   - ``pip install requests``


**3. Control Room Access** 
   - Ensure you have a Control Room **Username** and an **API key** for a user with access to the bot folders that need to be analyzed.
   - Users with the AAE_Admin role or users with the View everyone audit log actions permission can view audit logs for the Control Room.
	- https://docs.automationanywhere.com/bundle/enterprise-v2019/page/audit-api-supported.html


## Inputs

To run the utility, the following inputs are required:

![image](https://github.com/user-attachments/assets/dd861a97-22c8-43f2-b273-3f68be44088f)

   - **Control Room URL**: The control room url for log retrieval.
   - **Credentials**: Authentication details (Username & APIKey) to access audit logs securely.
   - **Starttime** and **Endtime** :  The date range for log extraction, specified in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
   - ``Example: 2025-03-28T06:18:33Z``

## Process Flow
   - User provides input details:
	- Control Room details
	- Credentials for authentication
	- Date range
	- Output folder path

   - Utility fetches logs in batches of 400 records:
	- Retrieves the first batch and exports it to a CSV file.
	- Increments the offset and fetches the next batch.
	- Appends the new batch to the CSV file.
   - Logs activity and errors:
	- Generates a log file to track the progress and handle any errors.
   - Process continues until all logs are exported.


## Output

![image](https://github.com/user-attachments/assets/d867f786-e554-44af-95ca-cc949bc4c764)

   - **CSV File**: Contains all fetched logs structured by date range (filename  : Auditlogs.csv) .
   - **Log File**: Stores details of executed operations, errors, and processing information (filename : fetchAuditLogs.log).

## Use Case

   - This utility is ideal for organizations that need to extract and analyze audit logs systematically. The batch-based approach ensures efficiency while preventing system overload.


## Note
This audit log export utility simplifies log retrieval and management by automating the process. With its structured approach, users can efficiently extract and analyze audit logs while ensuring data integrity and security.

         
