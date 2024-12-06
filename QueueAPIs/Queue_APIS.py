import requests
import time
import math
import json

# Input configuration
input_config = {
    "DormantQueueDetails": [
        {"QueueID": "202", "TemplateID": "217"},
        {"QueueID": "201", "TemplateID": "216"},
        {"QueueID": "200", "TemplateID": "215"}
    ]
}

# Base URLs for templates and work items
BASE_TEMPLATE_URL = "https://aa-se-ind-5.my.automationanywhere.digital/v3/wlm/workitemmodels/"
BASE_WORK_ITEM_URL = "https://aa-se-ind-5.my.automationanywhere.digital/v3/wlm/queues/"
AUTOMATION_API_URL = "https://aa-se-ind-5.my.automationanywhere.digital/v3/wlm/automations/list"
cached_token = None
token_expiry = 0

def get_token(url, payload):
    global cached_token, token_expiry

    # Check if the token is valid
    if cached_token and time.time() < token_expiry:
        return cached_token

    try:
        # Make the POST request
        response = requests.post(url, json=payload)

        # Check the response status
        if response.status_code == 200:
            json_response = response.json()

            # Extract the token and expiry
            if 'token' in json_response:
                cached_token = json_response['token']
                token_expiry = time.time() + 3600
                return cached_token
            else:
                return "Error: 'token' attribute not found in the response."

        else:
            return f"Error: Status code {response.status_code}, Response: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# Function to fetch template attributes
def fetch_template_attributes(url_token,body_token,template_id):
    url = f"{BASE_TEMPLATE_URL}{template_id}"
    token = get_token(url_token,body_token)
    headers = {"X-Authorization": token}
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        data = response.json()
        return {f"col{i+1}": attr["name"] for i, attr in enumerate(data.get("attributes", []))}
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch template {template_id} from {url}: {e}")
        return {}

# Function to fetch work items with payload
def fetch_work_items(url_token, body_token,queue_id, payload_dormant):
    url = f"{BASE_WORK_ITEM_URL}{queue_id}/workitems/list"
    token = get_token(url_token,body_token)
    headers = {"X-Authorization": token}
    try:
        response = requests.post(url, json=payload_dormant,headers=headers)
        response.raise_for_status()
        json_response = response.json()
        # print(json_response)
        if 'list' in json_response:
            # print(queue_id+str(json_response['list']))
            return json_response['list']
        # return response.json()  # Assuming API returns work items in JSON format
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch work items for queue {queue_id} from {url}: {e}")
        return []

def fetch_bot_ID(url_token, body_token,queue_id, payload_dormant):

    bot_url = 'https://aa-se-ind-5.my.automationanywhere.digital/v2/repository/files/'


    token = get_token(url_token,body_token)
    headers = {"X-Authorization": token}
    try:
        response = requests.post(AUTOMATION_API_URL, json=payload_dormant,headers=headers)
        response.raise_for_status()
        json_response = response.json()
        # print(json_response['list'][0]['fileId'])
        if 'list' in json_response:
            # print(json_response["list"][0]["poolId"])
            # print(json_response['list'][0]['fileId'])
            response = requests.get(bot_url+json_response['list'][0]['fileId'], headers=headers)
            if response.status_code==200:
                json_response = response.json()
            both_path = json_response.get('path')
            both_path = both_path.replace("Automation Anywhere\\", "")

            return both_path
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch work items for queue {queue_id} from {AUTOMATION_API_URL}: {e}")
        return []


def dormant_api_devices_fetch(url_token, body_token,payload_device,device_url):
    token = get_token(url_token,body_token)

    headers = {"X-Authorization": token}
    try:
        response = requests.post(AUTOMATION_API_URL, json=payload_device, headers=headers)
        if response.status_code == 200:  # Adjust based on your API's success status code
            json_response = response.json()
            if 'list' in json_response:
                # print(json_response["list"][0]["poolId"])
                response = requests.get(device_url+json_response["list"][0]["poolId"], headers=headers)
                if response.status_code==200:
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

# Function to map work item columns to attribute names
def map_work_items_to_template(work_items, column_mapping):
    mapped_items = []
    for item in work_items:
        mapped_item = {column_mapping[key]: item[key] for key in column_mapping if key in item}
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
    # Sort the items first by the primary priority column (e.g., WiP), then by the secondary (e.g., SiP)
    sorted_items = sorted(work_items, key=lambda x: tuple(x.get(col, 0) for col in priority_columns))
    # print(sorted_items)
    return sorted_items

# Function to process, score, and sort work items
def fetch_and_process_all_work_items(url_token,body_token,payload,input_config,payload_device,priority_columns,device_base_url):
    all_results = []  # List to store results for all queues

    # Loop through each queue in the input configuration
    for detail in input_config["DormantQueueDetails"]:
        queue_id = detail["QueueID"]
        template_id = detail["TemplateID"]

        # Example: Fetch work items (similar logic to your previous code)
        work_items = fetch_work_items(url_token, body_token,queue_id,payload) # Use the previously defined function

        # Map columns to template attributes (use your existing column_mapping function)
        column_mapping = fetch_template_attributes(url_token,body_token,template_id)  # Fetch attribute mappings
        mapped_items = map_work_items_to_template(work_items, column_mapping)

        # Sort the mapped work items based on dynamic priority columns (WiP and SiP)
        sorted_items = sort_work_items(mapped_items, priority_columns)

        # Dynamically prepare the payload for the dormant API call (using queue_id)
        payload_dev = payload_device.copy()  # Copy the base payload template
        payload_dev["filter"]["value"] = queue_id  # Update the queueId in the payload

        # Fetch the device count using the API and payload
        device_count = dormant_api_devices_fetch(url_token, body_token,payload_dev,device_base_url)
        bot_id = fetch_bot_ID(url_token, body_token,queue_id, payload_dev)

        # Append the result for this queue to the final results list
        all_results.append({
            "QueueID": queue_id,
            "DeviceCount": device_count,
            "BotID":bot_id,
            "WorkItems": sorted_items
        })
    print(all_results)
    return all_results

## Update Logic Start

# Function to count number of devices in active Q
def device_count_api(url_token, body_token,device_pool_url):
    token = get_token(url_token,body_token)
    headers = {"X-Authorization": token}
    try:
        # Make the POST requestet(device_pool_url ,headers=headers)
        response = requests.get(device_pool_url,headers=headers)
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

# Counting ready to run items in active Q
def count_ready_to_run(url_token, body_token,url_active, body_active):
    ##url
    ## url_active = "https://aa-se-ind-5.my.automationanywhere.digital/v3/wlm/queues/192/workitems/list"
    token = get_token(url_token,body_token)
    headers = {"X-Authorization": token}

    try:
        # Make the POST request
        response = requests.post(url_active, json=body_active, headers=headers)

        # Raise an error if the response is not successful
        response.raise_for_status()

        # Parse the response JSON
        response_data = response.json()

        # Ensure 'list' key exists in the response
        if 'list' not in response_data:
            print("Error: 'list' key not found in the response.")
            return 0

        # Count the number of items with status 'READY_TO_RUN'
        items = response_data['list']
        ready_to_run_count = sum(1 for item in items if item.get("status") == "READY_TO_RUN")

        return ready_to_run_count

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return 0

# Data that can be filled based device pool minus ready_to_run
def num_to_fill(url_token, body_token,url_active, body_active,device_pool_api):
    count = device_count_api(url_token,body_token,device_pool_api)-count_ready_to_run(url_token, body_token,url_active, body_active)
    return count

# Distribute items across queues based on device count
def allocate_items_based_on_ratio(url_token,body_token,payload,input_config,payload_device,priority_columns,device_base_url,url_active, body_active,device_pool_api):
    all_results = fetch_and_process_all_work_items(url_token,body_token,payload,input_config,payload_device,priority_columns,device_base_url)
    num_items = num_to_fill(url_token, body_token,url_active, body_active,device_pool_api)
    total_device_count = sum(result["DeviceCount"] for result in all_results)
    if total_device_count == 0:
        print("Warning: Total device count is zero. Cannot distribute items.")
        return []

    distributed_items = []
    for result in all_results:
        queue_id = result["QueueID"]
        device_count = result["DeviceCount"]
        work_items = result["WorkItems"]
        bot_id = result["BotID"]

        # Calculate number of items to allocate
        allocation_count = int((device_count / total_device_count) * num_items)
        for item in work_items[:allocation_count]:
            distributed_items.append({**item, 'BotID': bot_id})
        # distributed_items.extend(work_items[:allocation_count])
        # print(f"Queue {queue_id}: Allocated {allocation_count} items.")
    print("Distribute Data" +(str)(distributed_items))
    return distributed_items

def sort_allocated_data(url_token,body_token,payload,input_config,payload_device,priority_columns,device_base_url,url_active, body_active,device_pool_api):

    data = allocate_items_based_on_ratio(url_token,body_token,payload,input_config,payload_device,priority_columns,device_base_url,url_active, body_active,device_pool_api)
    # Filter data to include only entries with both 'WiP' and 'SiP'
    filtered_data = [entry for entry in data if 'WiP' in entry]

    # Sort based on 'WiP' first and 'SiP' second in ascending order
    sorted_data = sorted(filtered_data, key=lambda x: (int(x['WiP']), int(x.get('SiP', 0))))
    print("Sorted Data" +(str)(sorted_data))
    # Return the sorted list
    return sorted_data


def prepare_payload_from_work_items(url_token, body_token, payload, input_config, payload_device, priority_columns, device_base_url, url_active, body_active, device_pool_api):
    """
    Prepares a payload from the distributed items for an API request.

    Args:
        url_token: URL token for allocation logic.
        body_token: Body token for allocation logic.
        payload: Initial payload template.
        input_config: Configuration for the payload.
        payload_device: Device-specific configuration.
        priority_columns: Columns used to prioritize work items.
        device_base_url: Base URL for devices.
        url_active: Active URL configuration.
        body_active: Active body configuration.
        device_pool_api: API for the device pool.

    Returns:
        dict: A payload dictionary with a "workItems" key containing formatted items.
    """
    # Call allocation function to get distributed items
    distributed_items = sort_allocated_data(
        url_token, body_token, payload, input_config, payload_device, priority_columns, device_base_url, url_active, body_active, device_pool_api
    )
    payload = {"workItems": []}

    for entry in distributed_items:
        # Convert the entry to a string format for ReferenceID
        reference_id = str(entry).replace("'", '"')  # replace single quotes with double quotes for JSON consistency
        bot_path = entry.get('BotID', '')  # Get BotID
        work_item = {
            "json": {
                "Body": reference_id,
                "BotPath": bot_path,
                "ProcessPriority": 0,
                "WorkitemPriority": 0,
                "Score": 1
            }
        }
        payload["workItems"].append(work_item)
        print("payload"+(str)(payload))
        return payload



## Posting to active Q
def invoke_api(url_token,body_token,payload,input_config,payload_device,priority_columns,device_base_url,url_active, body_active,device_pool_api,active_post_url):
    token = get_token(url_token,body_token)
    json_payload = prepare_payload_from_work_items(url_token,body_token,payload,input_config,payload_device,priority_columns,device_base_url,url_active, body_active,device_pool_api)
    # print(json_payload)
    headers = {"Content-Type": "application/json","X-Authorization": token}

    try:
        # Make the POST request
        response = requests.post(active_post_url, json=json_payload, headers=headers)

        # Check the response status
        if response.status_code == 200:  # Adjust based on your API's success status code
            json_response = response.json()
            return json_response
        else:
            return f"Error: Status code {response.status_code}, Response: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


# Main process
def main():
    # Prepare mappings from input configuration
    url_token = 'https://aa-se-ind-5.my.automationanywhere.digital/v2/authentication'
    body_token = {
        "username": "syed",
        "password": "password"
    }
    device_base_url = 'https://aa-se-ind-5.my.automationanywhere.digital/v2/devices/pools/'
    payload_work_iem = {"sort":[{"field":"computedStatus","direction":"asc"}],"filter":{},"fields":[],"page":{"length":100,"offset":0}}
    payload_device ={
        "fields": [],
        "filter": {"operator": "eq", "value": "", "field": "queueId"},
        "page": {"offset": 0, "length": 1, "total": 0, "totalFilter": 0},
        "sort": []
    }
    priority_columns = ["WiP", "SiP"]
    url_active= "https://aa-se-ind-5.my.automationanywhere.digital/v3/wlm/queues/197/workitems/list"
    body_active = {"sort":[{"field":"computedStatus","direction":"asc"}],"filter":{},"fields":[],"page":{"length":100,"offset":0}}
    device_url = 'https://aa-se-ind-5.my.automationanywhere.digital/v2/devices/pools/360'
    active_post_url = 'https://aa-se-ind-5.my.automationanywhere.digital/v3/wlm/queues/207/workitems'
    # final_work_items = fetch_and_process_all_work_items(url_token,body_token,payload_work_iem,input_config,payload_device,priority_columns,device_base_url)
    #num_to_fill = 9  # Replace with actual function call

    # Distribute items
    # print(final_work_items)
    # distributed_items = allocate_items_based_on_ratio(url_token,body_token,payload_work_iem,input_config,payload_device,priority_columns,device_base_url,url_active, body_active,device_url)
    # payload_for_active_Q = queue_restructuring(url_token,body_token,payload_work_iem,input_config,payload_device,priority_columns,device_base_url,url_active, body_active,device_url)
    # print("Distributed Items:", queue_restructuring)
    # print("payload for active Q",payload_for_active_Q)
    post_result = invoke_api(url_token,body_token,payload_work_iem,input_config,payload_device,priority_columns,device_base_url,url_active, body_active,device_url,active_post_url)
    print(post_result)
    # queue_id = 201
    # payload_dormant ={"fields":[],"filter":{"operator":"eq","value":"201","field":"queueId"},"page":{"offset":0,"length":1,"total":0,"totalFilter":0},"sort":[]}
    # print(fetch_bot_ID(url_token, body_token,queue_id, payload_dormant))

if __name__ == "__main__":
    main()
