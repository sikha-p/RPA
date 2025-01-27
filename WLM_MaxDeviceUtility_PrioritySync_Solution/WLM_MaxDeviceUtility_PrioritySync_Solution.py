# ********************************************#
# *****Author : Sikha Poyyil ******************#
# ********************************************#
import json
import os
import tempfile
import requests
import time
import inspect
import logging
import sys
import json
import traceback
import pandas as pd
from datetime import datetime, timedelta
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Global variables defined
logger = logging.getLogger(__name__)
BASE_CR_URL = ""
FEEDER_QUEUE_DETAILS = []
AUTH_CREDENTIALS = {}
PRIORITY_COLUMNS = []
ACTIVE_QUEUE_ID = ""
ACTIVE_QUEUE_POOL_ID = 0
cached_token = None
token_expiry = 0
PAYLOAD_WORKITEM = {"sort": [],
                    "filter": {"operator": "eq", "value": "NEW", "field": "status"}, "fields": [],
                    "page": {"length": 100, "offset": 0}}
PAYLOAD_AUTOMATIONS = {
    "fields": [],
    "filter": {"operator": "eq", "value": "", "field": "queueId"},
    "page": {"offset": 0, "length": 1, "total": 0, "totalFilter": 0},
    "sort": []
}


# Function to fetch auth token using CR API
def get_token():
    auth_url = BASE_CR_URL + "/v2/authentication"
    global cached_token, token_expiry
    # Check if the token is valid
    if cached_token and time.time() < token_expiry:
        return cached_token
    try:
        # Make the POST request
        response = requests.post(auth_url, json=AUTH_CREDENTIALS)
        # Check the response status
        if response.status_code == 200:
            json_response = response.json()
            # Extract the token and expiry
            if 'token' in json_response:
                cached_token = json_response['token']
                token_expiry = time.time() + 3600
                return cached_token
            else:
                log("Error: 'token' attribute not found in the response.", "debug")
                return "Error: 'token' attribute not found in the response."
        else:
            log(f"Error: Status code {response.status_code}, Response: {response.text}", "debug")
            return f"Error: Status code {response.status_code}, Response: {response.text}"
    except requests.exceptions.RequestException as e:
        log(f"/v2/authentication request failed : {e}", "debug")
        return f"Request failed: {e}"


# Function to fetch template attributes
def fetch_template_attributes(template_id):
    url = f"{BASE_CR_URL}/v3/wlm/workitemmodels/{template_id}"
    token = get_token()
    headers = {"X-Authorization": token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {f"col{i + 1}": attr["name"] for i, attr in enumerate(data.get("attributes", []))}
    except requests.exceptions.RequestException as e:
        log(f"Failed to fetch template {template_id} from {url}: {e}", "debug")
        return {}


# Function to fetch work items with payload
def fetch_work_items(queue_id, payload_dormant):
    url = f"{BASE_CR_URL}/v3/wlm/queues/{queue_id}/workitems/list"
    token = get_token()
    headers = {"X-Authorization": token}
    try:
        response = requests.post(url, json=payload_dormant, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        if 'list' in json_response:
            return json_response['list']
    except requests.exceptions.RequestException as e:
        log(f"Failed to fetch work items for queue {queue_id} from {url}: {e}", "debug")
        return []


# Function to fetch bot ID associated with a Queue automation
def fetch_automations_by_queueid(queue_id, payload_dormant):
    token = get_token()
    headers = {"X-Authorization": token}
    try:
        response = requests.post(BASE_CR_URL + "/v3/wlm/automations/list", json=payload_dormant, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        if 'list' in json_response:
            fileID = json_response['list'][0]['fileId']
            poolID = json_response['list'][0]['poolId']
            response = requests.get(BASE_CR_URL + "/v2/repository/files/" + fileID, headers=headers)
            if response.status_code == 200:
                json_response = response.json()
            bot_path = json_response.get('path')
            bot_path = bot_path.replace("Automation Anywhere\\", "")
            log(f"Bot associated with queue. Bot path: {bot_path}, PoolID: {poolID}", "debug")
            return {"bot_path": bot_path, "poolId": poolID}
    except requests.exceptions.RequestException as e:
        log(f"Failed to fetch work items for queue {queue_id} from {BASE_CR_URL}/v3/wlm/automations/list: {e}", "debug")
        return []


# Function to create queue and workitems list
def create_queue_workitem_list(data):
    result = []
    # Loop through each item in the data and group by feederQueueID
    for item in data:
        queue_id = item['feederQueueID']
        work_item_id = item['feederQueueWorkItemID']
        # Check if the queue ID already exists in the result
        existing_queue = next((queue for queue in result if queue['queueid'] == str(queue_id)), None)

        if existing_queue:
            # If queue already exists, append the work item ID to the workitems list
            existing_queue['workitems'].append(work_item_id)
        else:
            # If queue doesn't exist, create a new entry
            result.append({
                'queueid': str(queue_id),
                'workitems': [work_item_id]
            })
    return result


def group_workitems_by_queueid(data):
    # To store the final output
    queue_grouped_data = {}

    # Loop through the work items
    for item in data["workItems"]:
        # Parse the JSON string inside the 'Body' key
        body = item["json"]["Body"]
        body_dict = json.loads(body)  # Convert the Body string into a dictionary

        # Extract the 'feederQueueID' and 'feederQueueWorkItemID'
        queue_id = body_dict.get("feederQueueID")
        workitem_id = body_dict.get("feederQueueWorkItemID")

        # If the queue_id is not already in the dictionary, add it
        if queue_id not in queue_grouped_data:
            queue_grouped_data[queue_id] = {"queueid": queue_id, "workitems": []}

        # Append the workitem_id to the corresponding queue's workitems list
        queue_grouped_data[queue_id]["workitems"].append(workitem_id)

    # Convert the dictionary to a list of values (to match the output structure)
    result = list(queue_grouped_data.values())
    return result


# Function to update the workitem status as update after adding it to the Active Queue
def update_workitem_status(workitemsGroupByQueue, status, null=None):
    token = get_token()
    for item in workitemsGroupByQueue:

        json_payload = {"status": status, "ids": item['workitems'], "deferredType": "INDEFINITELY",
                        "deferredUntil": null}
        headers = {"Content-Type": "application/json", "X-Authorization": token}
        apiUrl = BASE_CR_URL + "/v3/wlm/queues/" + item['queueid'] + "/workitems/updateStatus"
        try:
            # Make the POST request
            response = requests.post(apiUrl, json=json_payload, headers=headers)

            # Check the response status
            if response.status_code == 200:  # Adjust based on your API's success status code
                json_response = response.json()
                # return json_response
            else:
                log(f"Error: Status code {response.status_code}, Response: {response.text}", "debug")
                return f"Error: Status code {response.status_code}, Response: {response.text}"
        except requests.exceptions.RequestException as e:
            log(f"Request failed: {e}", "debug")
            return f"Request failed: {e}"


def invoke_api(api_url, method, payload):
    token = get_token()
    headers = {"X-Authorization": token}
    try:
        if method == "post":
            response = requests.post(api_url, json=payload, headers=headers)
            print(response)
        elif method == "get":
            response = requests.get(api_url, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        log(f"Failed while invoking api  {api_url} using payload {payload}: {e}", "debug")
        return []


# Function to map work item columns to attribute names
def map_work_items_to_template(work_items, column_mapping, Score):
    mapped_items = []
    for item in work_items:
        mapped_item = {column_mapping[key]: item[key] for key in column_mapping if key in item}
        mapped_item["feederQueueWorkItemID"] = item["id"]
        mapped_item["feederQueueID"] = item["queueId"]
        mapped_item["Score"] = Score
        mapped_items.append(mapped_item)
    return mapped_items


# Function to sort work items based on dynamic priority columns
def sort_work_items(work_items, priority_columns):
    """
    Sort the work items based on the provided priority columns.
    The items are sorted in descending order for each of the specified columns.

    :param work_items: List of work items (dictionaries)
    :param priority_columns: List of column names to sort by, in order of priority
    :return: Sorted list of work items
    """
    # Sort the items first by the primary priority column (e.g., WorkItemPriority), then by the secondary (e.g., ProcessPriority)
    sorted_items = sorted(work_items, key=lambda x: tuple(x.get(col, 0) for col in priority_columns))
    return sorted_items


def dormant_api_devices_fetch(payload_dev):
    try:

        response = invoke_api(f"{BASE_CR_URL}/v3/wlm/automations/list", "post", payload_dev)
        if response.status_code == 200:  # Adjust based on your API's success status code
            json_response = response.json()
            if 'list' in json_response:
                poolID = json_response["list"][0]["poolId"]
                ACTIVE_QUEUE_POOL_ID = poolID
                response = invoke_api(f"{BASE_CR_URL}/v2/devices/pools/{poolID}", "get", "")
                if response.status_code == 200:
                    json_response = response.json()
                    device_ids = json_response.get('deviceIds', [])
                    device_count = len(device_ids)
                    return device_count
                else:
                    return "Error: 'token' attribute not found in the response."
        else:
            return f"Error: Status code {response.status_code}, Response: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def getDevices_count_by_poolID(poolId):
    token = get_token()
    headers = {"X-Authorization": token}
    device_pool_url = f"{BASE_CR_URL}/v2/devices/pools/{poolId}"
    try:
        response = requests.get(device_pool_url, headers=headers)
        if response.status_code == 200:  # Adjust based on your API's success status code
            json_response = response.json()
            device_ids = json_response.get('deviceIds', [])
            device_count = len(device_ids)
            return device_count
        else:
            return f"Error: Status code {response.status_code}, Response: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    # return 5


def device_count_api():
    token = get_token()
    headers = {"X-Authorization": token}
    # GET ACTIVE QUEUES AUTOMATION'S DEVICE POOL ALLOCATED
    device_pool_url = f"{BASE_CR_URL}/v2/devices/pools/368"
    try:
        # Make the POST requestet(device_pool_url ,headers=headers)
        response = requests.get(device_pool_url, headers=headers)
        if response.status_code == 200:  # Adjust based on your API's success status code
            json_response = response.json()
            device_ids = json_response.get('deviceIds', [])
            device_count = len(device_ids)
            return device_count
        else:
            return f"Error: Status code {response.status_code}, Response: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


# Function to get all NEW workitems (unprocessed) from the feeder queues (dormant queues)
def fetch_unprocessed_workitems_from_feederqueues(Queues):
    all_results = []  # List to store results for all queues

    # Loop through each queue in the input configuration
    for detail in Queues:
        queue_id = detail["QueueID"]
        score = detail["CycleTime"]
        # GET TEMPLATE ID FROM QUEUE ID
        template_id = detail["TemplateID"]
        # Dynamically prepare the payload for the dormant API call (using queue_id)
        payload_dev = PAYLOAD_AUTOMATIONS.copy()  # Copy the base payload template
        payload_dev["filter"]["value"] = queue_id  # Update the queueId in the payload
        bot_details = fetch_automations_by_queueid(queue_id, payload_dev)
        bot_path = bot_details["bot_path"]
        poolId = bot_details["poolId"]
        DevicesCountInPool = getDevices_count_by_poolID(poolId)
        # Map columns to template attributes (use your existing column_mapping function)
        column_mapping = fetch_template_attributes(template_id)  # Fetch attribute mappings
        # Get the key for WorkItemPriority from column_mapping object
        key = next((k for k, v in column_mapping.items() if v == WORKITEMPRIORITYKEY), None)
        PAYLOAD_WORKITEM["sort"] = [{"field": key, "direction": "asc"}]
        PAYLOAD_WORKITEM["page"]["length"] = DevicesCountInPool

        # Example: Fetch work items (similar logic to your previous code)
        work_itemsAPIResponse = invoke_api(f"{BASE_CR_URL}/v3/wlm/queues/{queue_id}/workitems/list", "post",
                                           PAYLOAD_WORKITEM)  # Use the previously defined function
        if work_itemsAPIResponse.status_code == 200:
            json_response = work_itemsAPIResponse.json()
            if 'list' in json_response:
                work_items = json_response['list']

        mapped_items = map_work_items_to_template(work_items, column_mapping, score)
        sorted_items = sort_work_items(mapped_items, PRIORITY_COLUMNS)
        # Append the result for this queue to the final results list
        all_results.append({
            "QueueID": queue_id,
            "DeviceCount": DevicesCountInPool,
            "BotPath": bot_path,
            "WorkItems": sorted_items
        })
    sorted_items = sort_work_items(all_results, PRIORITY_COLUMNS)
    log(f"fetch_unprocessed_workitems_from_feederqueues - sorted Items : {json.dumps(sorted_items)}", "debug")
    return sorted_items


def allocation_loop(all_results, distributed_items, total_device_count, no_of_available_devices):
    for result in all_results:
        ueue_id = result["QueueID"]
        device_count = result["DeviceCount"]
        work_items = result["WorkItems"]
        BotPath = result["BotPath"]
        allocation_count = int((device_count / total_device_count) * no_of_available_devices)
        allocated_items = work_items[:allocation_count]
        for item in allocated_items:
            distributed_items.append({**item, 'BotPath': BotPath})
            work_items.remove(item)
        result["WorkItems"] = work_items
        workitemsGroupByQueue = create_queue_workitem_list(distributed_items)
        update_workitem_status(workitemsGroupByQueue, "ON_HOLD")
    return distributed_items, all_results


def getTotalItems(all_results):
    # Assuming all_results is a list where each item has a 'work_items' attribute
    total_items = 0

    # Loop through all items in the all_results list
    for result in all_results:
        # Check if 'work_items' exists and is a list
        total_items += len(result['WorkItems'])
    return total_items


def get_high_priority_workitems(required_count, queues):
    # Collect all work items with their priorities along with their parent QueueID
    all_workitems = []
    for queue in queues:
        for item in queue['WorkItems']:
            all_workitems.append({
                'QueueID': queue['QueueID'],
                'DeviceCount': int(queue['DeviceCount']),
                'BotPath': queue['BotPath'],
                'WorkItem': item
            })

    # Sort work items by ProcessPriority (ascending) and WorkItemPriority (ascending)
    all_workitems.sort(
        key=lambda x: (int(x['WorkItem']['ProcessPriority']), int(x['WorkItem']['WorkItemPriority']))
    )

    # Pick the required number of work items
    selected_workitems = all_workitems[:required_count]

    # Create the output structure in the same format as the input
    result = {}
    for workitem in selected_workitems:
        queue_id = workitem['QueueID']
        if queue_id not in result:
            result[queue_id] = {
                'QueueID': queue_id,
                'DeviceCount': workitem['DeviceCount'],
                'BotPath': workitem['BotPath'],
                'WorkItems': []
            }
        result[queue_id]['WorkItems'].append(workitem['WorkItem'])

    # Convert the result dictionary to a list of queues
    return list(result.values())


def total_workitems(queues):
    # Initialize counter for work items
    total_items = 0

    # Loop through each queue and sum the number of work items
    for queue in queues:
        total_items += len(queue.get('WorkItems', []))

    return total_items


def allocate_items_based_on_ratio(all_results):
    counter = 0
    total_device_count = sum(result["DeviceCount"] for result in all_results)
    payload_dev = PAYLOAD_AUTOMATIONS.copy()  # Copy the base payload template
    payload_dev["filter"]["value"] = ACTIVE_QUEUE_ID  # Update the queueId in the payload
    active_queue_automation_details = fetch_automations_by_queueid(ACTIVE_QUEUE_ID, PAYLOAD_AUTOMATIONS)
    no_of_available_devices = total_device_count
    if total_device_count == 0:
        print("Warning: Total device count is zero. Cannot distribute items.")
        return []

    distributed_items = []
    while (len(distributed_items) < no_of_available_devices):
        log(f"Distributed items count {str(len(distributed_items))} , No of available devices : {str(no_of_available_devices)}",
            "debug")
        # Update all the workitems inside distributed_items's status as ON_HOLD to avoid pick those in the next iteration.
        if (getTotalItems(all_results) == 0):
            log("whole workitems count = 0", "debug")
            # get the queues which are not in the current list and there in the config
            includedQueueIDs = list({int(item['QueueID']) for item in all_results})
            df = pd.read_csv(CSV_FILE_NAME)

            # Extract the 'QueueID' column
            allQueueIDs = (df['QueueID']).tolist()
            remainingQueueIDs = [queue_id for queue_id in allQueueIDs if queue_id not in includedQueueIDs]
            remainingQueueIDs = [str(queue_id) for queue_id in remainingQueueIDs]
            # Get the difference between no of available devices - len(distributed item)
            dif = no_of_available_devices - len(distributed_items)
            if len(remainingQueueIDs) == 0:
                newItems = fetch_unprocessed_workitems_from_feederqueues(FEEDER_QUEUE_DETAILS)
            else:
                # Get 'dif' no of workitems from the new set of queues based on Workitem & process Priority
                QueueDetails = [item for item in FEEDER_QUEUE_DETAILS if item['QueueID'] in remainingQueueIDs]
                newItems = fetch_unprocessed_workitems_from_feederqueues(QueueDetails)
            if total_workitems(newItems) == 0:
                for queue in newItems:
                    all_results.append(queue)
                counter += 1
                print("Counter incremented", str(counter))
                if counter == no_of_available_devices:
                    break
                # break
            else:
                newItems2 = get_high_priority_workitems(dif, newItems)
                for queue in newItems2:
                    all_results.append(queue)

            print(all_results)
        distributed_items, all_results = allocation_loop(all_results, distributed_items, total_device_count,
                                                         no_of_available_devices)
    log(f"Distribute Data : {json.dumps(distributed_items)}", "debug")
    return distributed_items


def sort_allocated_data(data):
    # Filter data to include only entries with both 'WorkItemPriority' and 'ProcessPriority'
    sorted_data = sorted(data, key=lambda x: tuple(x.get(col, 0) for col in ["ProcessPriority"]))
    print("Sorted Data" + (str)(sorted_data))
    # Return the sorted list
    return sorted_data


def sort_and_add_workitems_to_activequeue_from_feederqueues(queues):
    all_results = fetch_unprocessed_workitems_from_feederqueues(queues)

    distributed_items = allocate_items_based_on_ratio(all_results)
    # Call allocation function to get distributed items
    distributed_items_sorted = sort_allocated_data(distributed_items)

    payload = {"workItems": []}
    for entry in distributed_items_sorted:
        # Convert the entry to a string format for ReferenceID
        reference_id = str(entry).replace("'", '"')  # replace single quotes with double quotes for JSON consistency
        bot_path = entry.get('BotPath', '')  # Get BotID
        work_item = {
            "json": {
                "Body": reference_id,
                "BotPath": bot_path,
                "ProcessPriority": entry['ProcessPriority'],
                "WorkitemPriority": entry['WorkItemPriority'],
                "Score": entry['Score']
            }
        }
        payload["workItems"].append(work_item)

    token = get_token()
    headers = {"Content-Type": "application/json", "X-Authorization": token}

    try:
        print("FINAL payload" + (str)(payload))
        # Make the POST request
        response = requests.post(f"{BASE_CR_URL}/v3/wlm/queues/{ACTIVE_QUEUE_ID}/workitems", json=payload,
                                 headers=headers)

        # Check the response status
        if response.status_code == 201:  # Adjust based on your API's success status code
            json_response = response.json()
            # Update Workitem status in feederQueues as COMPLETED
            workitemsGroupByQueue = group_workitems_by_queueid(payload)
            update_workitem_status(workitemsGroupByQueue, "COMPLETED")
            # Update lastPoll
            unique_feeder_queue_ids = set(
                item['json']['Body'].split('"feederQueueID": ')[1].split(',')[0].strip('"')
                for item in payload['workItems']
            )
            updateLastPoll(CSV_FILE_NAME, unique_feeder_queue_ids)

            return json_response
        else:
            return f"Error: Status code {response.status_code}, Response: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def sort_and_add_workitems_to_activequeue_from_feederqueues2(queues):
    all_results = fetch_unprocessed_workitems_from_feederqueues(queues)

    distributed_items = allocate_items_based_on_ratio(all_results)
    # Call allocation function to get distributed items
    distributed_items_sorted = sort_allocated_data(distributed_items)

    payload = {"workItems": []}
    for entry in distributed_items_sorted:
        # Convert the entry to a string format for ReferenceID
        reference_id = str(entry).replace("'", '"')  # replace single quotes with double quotes for JSON consistency
        bot_path = entry.get('BotPath', '')  # Get BotID
        work_item = {
            "json": {
                "Body": reference_id,
                "BotPath": bot_path,
                "ProcessPriority": entry['ProcessPriority'],
                "WorkitemPriority": entry['WorkItemPriority'],
                "Score": entry['Score']
            }
        }
        payload["workItems"].append(work_item)

    token = get_token()
    headers = {"Content-Type": "application/json", "X-Authorization": token}

    try:
        print("FINAL payload" + (str)(payload))
        # Make the POST request
        response = requests.post(f"{BASE_CR_URL}/v3/wlm/queues/{ACTIVE_QUEUE_ID}/workitems", json=payload,
                                 headers=headers)

        # Check the response status
        if response.status_code == 201:  # Adjust based on your API's success status code
            json_response = response.json()
            # Update Workitem status in feederQueues as COMPLETED
            workitemsGroupByQueue = group_workitems_by_queueid(payload)
            update_workitem_status(workitemsGroupByQueue, "COMPLETED")
            # Update lastPoll
            unique_feeder_queue_ids = set(
                item['json']['Body'].split('"feederQueueID": ')[1].split(',')[0].strip('"')
                for item in payload['workItems']
            )
            updateLastPoll(CSV_FILE_NAME, unique_feeder_queue_ids)

            return json_response
        else:
            return f"Error: Status code {response.status_code}, Response: {response.text}"
        # log(f"FINAL payload : {json.dumps(payload)}", "debug")
        # workitemsGroupByQueue = group_workitems_by_queueid(payload)
        # update_workitem_status(workitemsGroupByQueue, "COMPLETED")
        # # Update lastPoll
        # unique_feeder_queue_ids = set(
        #     item['json']['Body'].split('"feederQueueID": ')[1].split(',')[0].strip('"')
        #     for item in payload['workItems']
        # )
        # updateLastPoll(CSV_FILE_NAME, unique_feeder_queue_ids)

    except requests.exceptions.RequestException as e:
        log(f"Request failed: {e}", "debug")
        return f"Request failed: {e}"


# Initializing a logger with custom configuration
def initialize_logger(log_file_path, log_level):
    try:
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

            # Ensure the log file exists
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w'):  # Create the file
                pass
        # logger = logging.getLogger()
        logger.setLevel(getattr(logging, log_level.upper()))
        file_handler = logging.FileHandler(log_file_path, mode='a')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s (%(message)s',
                                      datefmt='(%d-%m-%Y %I.%M.%S %p)')

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        log("Log file started.", log_level)
    except Exception as err:
        send_notification(f"Error Details: {str(err)}")
        return err


def log(log_msg, log_level):
    # Automatically log the current function details.
    # Get the previous frame in the stack, otherwise it would be this function!!!
    func = inspect.currentframe().f_back.f_code

    # Dump the message + the name of this function to the log.
    logger.log(level=getattr(logging, log_level.upper(), None), msg='{0}): {1}'.format(func.co_name, log_msg))

# Function to send error email notifications

def send_notification(error):
    log("Please include the email send code as per your requirement","debug")
    log("sample code has been given in send_notification function","debug")
    log(f" Error inside send _notification {str(error)}","debug")
    # Email details
    # with open("config.json", "r") as file:
    #     config = json.load(file)
    # sender_email = config['sender_email']
    # receiver_email = config['receiver_email']
    # password = config['password']
    #
    # # Create the email
    # subject = "Error Notification from WLMQueueSolution"
    # body = f"An error occured in WLMQueueSolution Python script. Please find the details below, {error}"
    #
    # # Create a MIME object
    # message = MIMEMultipart()
    # message["From"] = sender_email
    # message["To"] = receiver_email
    # message["Subject"] = subject
    #
    # # Attach the body to the email
    # message.attach(MIMEText(body, "plain"))
    #
    # # Connect to the SMTP server
    # try:
    #     # Use Gmail's SMTP server
    #     server = smtplib.SMTP("smtp.gmail.com", 587)
    #     server.starttls()  # Upgrade connection to secure
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message.as_string())
    #     print("Email sent successfully!")
    # except Exception as e:
    #     print(f"Error: {e}")
    # finally:
    #     server.quit()


# Define a function to check conditions
def check_queue(row):
    if pd.isna(row['LastPoll']):  # If 'LastPoll' is empty
        return True
    else:
        cycle_time_seconds = row['CycleTime'] * 60
        if (row['LastPoll'] + timedelta(seconds=cycle_time_seconds)) < datetime.now():
            return True
        else:
            return False


# Function to check the Queue eligibilty based on the Last Poll
def checkQueueEligibilityBasedOnLastPoll(filename):
    df = pd.read_csv(filename)
    # Ensure 'LastPoll' is in datetime format

    df['LastPoll'] = pd.to_datetime(df['LastPoll'], format="%Y-%m-%d %H:%M:%S")
    # Apply the function to the DataFrame
    df['AddQueue'] = df.apply(check_queue, axis=1)
    eligibleQueueIDs = df[df['AddQueue'] == True]['QueueID'].tolist()
    eligibleQueueIDs = [str(queue_id) for queue_id in eligibleQueueIDs]
    return eligibleQueueIDs


def updateLastPoll(csvFileName, queueIDs):
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.read_csv(csvFileName)
        queueIDs = [int(queue_id) for queue_id in queueIDs]
        df.loc[df['QueueID'].isin(queueIDs), 'LastPoll'] = current_time
        # Save the updated DataFrame back to CSV
        df.to_csv(csvFileName, index=False)
    except Exception as err:
        tb = traceback.extract_tb(err.__traceback__)
        # Get the last entry in the traceback which contains the information about the error
        filename, lineno, _, _ = tb[-1]
        result = json.dumps({
            'code': 'python.exception',
            'details': '',
            'message': str(err),
            'line_number': lineno
        })
        log(str(result), 'info')
        send_notification(f"Error Details: {str(result)}")


def updateLastCron(filename):
    # Specify the headers for the CSV file
    headers = ["QueueID", "TemplateID", "CycleTime", "ProcessPriority", "LastPoll", "LastCron"]
    data = {
        "FeederQueueDetails": FEEDER_QUEUE_DETAILS
    }

    # Get the current time for LastCron
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the file exists
    if not os.path.exists(filename):
        # File does not exist: Create the file and add rows
        print(f"File '{filename}' does not exist. Creating and adding data...")
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()  # Write the headers

            # Loop through the array and add rows
            for item in data["FeederQueueDetails"]:
                item["LastPoll"] = ""  # Leave LastPoll empty
                item["LastCron"] = current_time  # Set LastCron to current time
                writer.writerow(item)
        print(f"File '{filename}' created successfully with data.")
    else:
        # File exists: Update LastCron for all rows
        print(f"File '{filename}' exists. Updating LastCron values...")
        # Read the current content of the file
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)  # Load all rows into memory
            headers = reader.fieldnames  # Get headers

        # Update the LastCron field for each row
        for row in rows:
            row["LastCron"] = current_time

        # Write the updated rows back to the file
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()  # Write headers
            writer.writerows(rows)  # Write updated rows
        print(f"File '{filename}' updated successfully.")


try:
    log_level = 'debug'
    home_dir = os.path.expanduser("~")
    temp_folder = tempfile.gettempdir()
    # Construct the Desktop folder path
    desktop_path = os.path.join(home_dir, "Desktop")
    log_file_path = temp_folder + "\\WLM_Queue_Optimized.log"

    initialize_logger(log_file_path=log_file_path, log_level=log_level)
    log('hello', 'debug')
    # Open and read the JSON file
    with open("config.json", "r") as file:
        config = json.load(file)


    BASE_CR_URL = config['base_cr_url']
    print(BASE_CR_URL)
    FEEDER_QUEUE_DETAILS = config['FeederQueueDetails']
    WORKITEMPRIORITYKEY = config['WorkItemPriorityKey']
    AUTH_CREDENTIALS = config['auth_credentials']
    ACTIVE_QUEUE_ID = config['active_queue_id']
    PRIORITY_COLUMNS = config['priority_columns']
    CSV_FILE_NAME = "PollReport.csv"

    # Create a csv file and add the QueueDetails rows in to it in t
    updateLastCron(CSV_FILE_NAME)

    # CheckEligibility
    eligibleQueueIDs = checkQueueEligibilityBasedOnLastPoll(CSV_FILE_NAME)
    filtered_feederQueues = [item for item in FEEDER_QUEUE_DETAILS if item['QueueID'] in eligibleQueueIDs]
    # updateLastPoll(CSV_FILE_NAME,eligibleQueueIDs)

    sort_and_add_workitems_to_activequeue_from_feederqueues2(filtered_feederQueues)


except Exception as err:
    tb = traceback.extract_tb(err.__traceback__)
    # Get the last entry in the traceback which contains the information about the error
    filename, lineno, _, _ = tb[-1]
    result = json.dumps({
        'code': 'python.exception',
        'details': '',
        'message': str(err),
        'line_number': lineno
    })
    log(str(result), 'info')
    send_notification(f"Error Details: {str(result)}")
