# Author: Sikha Poyyil
#         Global Solution Desk(GSD)
# Company: Automation Anywhere

# Note: Below external libraries to be installed for script to work.
# 1. Requests-toolbelt library to be installed using below cmd for BLM apis to work
#    Command: pip install requests-toolbelt
import tempfile
import sys
import os
import json
import traceback
import shutil
import inspect
import logging
import datetime as dt
from pathlib import Path
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Global variables defined
logger = logging.getLogger(__name__)
updates_json = None


# Log the messages using logging library
def log(log_msg, log_level):
    # Automatically log the current function details.
    # Get the previous frame in the stack, otherwise it would be this function!!!
    func = inspect.currentframe().f_back.f_code

    # Dump the message + the name of this function to the log.
    logger.log(level=getattr(logging, log_level.upper(), None), msg='{0}): {1}'.format(func.co_name, log_msg))


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
        #logger = logging.getLogger()
        logger.setLevel(getattr(logging, log_level.upper()))
        file_handler = logging.FileHandler(log_file_path, mode='a')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s (%(message)s',
                                      datefmt='(%d-%m-%Y %I.%M.%S %p)')

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        log("Log file started.", log_level)
    except Exception as err:
        return  err


# Get user token status - valid or invalid
def token_status(cr_url, user_token):
    headers = {"accept": "application/json"}

    log("Token status: no data", 'debug')
    log("Headers: " + str(headers), 'debug')
    log("URL: " + cr_url + '/v1/authentication/token?token=' + str(user_token)[0:20], 'debug')

    response = requests.get(cr_url + '/v1/authentication/token?token=' + user_token, headers=headers)

    # Checking if response status is 200
    if response.status_code == 200:
        json_obj = response.json()
        log('Token status: ' + str(json_obj.get('valid')), 'info')
        # print('Token status: ' + str(json_obj.get('valid')))
        return str(json_obj.get('valid'))

    else:
        # Returning error json object
        error_json_obj = response.json()
        log(error_json_obj, 'info')
        # print(str(error_json_obj))
        return error_json_obj


# Generate user token in A360 Control room
def generate_token(cr_url, username, password, api_key):
    if password == '' and api_key.strip() != '':
        # Api key is not null and password is null
        data = '{ \"username\": \"' + str(username) + '\", \"apiKey\": \"' + str(api_key) + '\"}'
        log("Generate token: data = " + '{ \"username\": \"*********\", \"apiKey\": \"*********\"}', 'debug')

    elif password != '' and api_key.strip() == '':
        # Password is not null and api key is null
        data = '{ \"username\": \"' + str(username) + '\", \"password\": \"' + str(password) + '\"}'
        log("Generate token: data = " + '{ \"username\": \"*********\", \"password\": \"*********\"}', 'debug')

    elif password != '' and api_key.strip() != '':
        # Password and api key both are not null
        data = '{ \"username\": \"' + str(username) + '\", \"apiKey\": \"' + str(api_key) + '\"}'
        log("Generate token: data = " + '{ \"username\": \"*********\", \"apiKey\": \"*********\"}', 'debug')

    else:
        # Password and api key both are null
        result = json.dumps({'code': 'user.credentials.empty', 'details': '',
                             'message': 'Both password and api key are null. Please provide either one of them to generate user token'})
        log(result, 'info')
        return result

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    log("Headers: " + str(headers), 'debug')
    log("URL: " + cr_url + '/v2/authentication', 'debug')

    response = requests.post(cr_url + '/v2/authentication', data=data, headers=headers)

    # Checking if response status is 200
    if response.status_code == 200:
        json_obj = response.json()

        # print("User Token: " + str(json_obj.get('token'))[0:20] + ".******")
        log("User Token: " + str(json_obj.get('token'))[0:20] + ".****** generated.", 'info')
        # Returning user token
        return json_obj.get('token')
    else:
        error_json_obj = response.json()

        # print(str(error_json_obj))
        # Returning error json object
        log(str(error_json_obj), 'info')
        return error_json_obj


# Export bot from A360 Control room
def export_bot(cr_url, user_token, export_bot_name, bot_ids):
    data = '{\"name\": \"' + str(export_bot_name) + '\", \"fileIds\": ' \
           + str(bot_ids) + ', \"includePackages\": false}, \"archivePassword\": \"A360@123\"}'

    headers = {"X-Authorization": user_token, 'Content-type': 'application/json', 'Accept': 'text/plain'}

    log("Export bot: " + str(data), 'debug')
    log("Headers: " + str(
        {"X-Authorization": user_token[0:20] + ".******", 'Content-type': 'application/json', 'Accept': 'text/plain'}),
        'debug')
    log("URL: " + cr_url + '/v2/blm/export', 'debug')

    response = requests.post(cr_url + '/v2/blm/export', data=data, headers=headers)

    # Checking if response status is 202
    if response.status_code == 202:
        json_obj = response.json()
        # print("Exported package request ID: " + str(json_obj.get('requestId')))
        log("Exported package request ID: " + str(json_obj.get('requestId')), 'info')
        return json_obj.get('requestId')

    else:
        error_json_obj = response.json()
        # print(str(error_json_obj))
        log(str(error_json_obj), 'info')
        # Returning error json object
        return error_json_obj


# Get bot package export status
def bot_export_status(cr_url, request_id, user_token):
    headers = {"X-Authorization": user_token, "accept": "application/json"}

    log("Export bot status: no data", 'debug')
    log("Headers: " + str({"X-Authorization": user_token[0:20] + ".******", 'Content-type': 'application/json'}),
        'debug')
    log("URL: " + cr_url + '/v2/blm/status' + request_id, 'debug')

    response = requests.get(cr_url + '/v2/blm/status/' + request_id, headers=headers)

    # Checking if response status is 200
    if response.status_code == 200:
        json_obj = response.json()

        # Checking bot export status
        if json_obj.get('status').lower() == 'completed':
            # print("Download file ID for the exported package: " + str(json_obj.get('downloadFileId')))
            log("Download file ID for the exported package: " + str(json_obj.get('downloadFileId')), 'info')

            # Returning download file id attribute
            return json_obj.get('downloadFileId')

        else:
            # Returning wait
            return 'wait'
    else:
        error_json_obj = response.json()

        # print(str(error_json_obj))
        log(str(error_json_obj), 'info')

        # Returning error json object
        return error_json_obj


# Import bot package into A360 Control room
def bot_import(cr_url, user_token, data_folder_path, data_file_name):
    multipart_data = MultipartEncoder(
        fields={
            # a file upload field
            'upload': (
                data_file_name, open(os.path.join(data_folder_path, data_file_name), 'rb'),
                'application/x-zip-compressed'),
            # plain text fields
            'actionIfExisting': 'OVERWRITE',
            'publicWorkspace': 'true',
            'archivePassword': 'A360@123'
        }
    )

    headers = {"X-Authorization": user_token, "Content-Type": multipart_data.content_type}

    log("Import bot: " + str({
        # a file upload field
        'upload': {'File Path: ' + os.path.join(data_folder_path, data_file_name), 'application/x-zip-compressed'},
        'actionIfExisting': 'OVERWRITE',
        'publicWorkspace': 'true',
        'archivePassword': 'A360@123'
    }), 'debug')
    log("Headers: " + str(
        {"X-Authorization": user_token[0:20] + ".******", "Content-Type": multipart_data.content_type}), 'debug')
    log("URL: " + cr_url + '/v2/blm/import', 'debug')

    response = requests.post(cr_url + '/v2/blm/import', headers=headers, data=multipart_data)

    # Checking if response status is 202
    if response.status_code == 202:
        json_obj = response.json()

        # print("Imported bot package request ID: " + str(json_obj.get('requestId')))
        log("Imported bot package request ID: " + str(json_obj.get('requestId')), 'info')

        return json_obj.get('requestId')
    else:
        error_json_obj = response.json()

        # print(str(error_json_obj))
        log(str(error_json_obj), 'info')

        # Returning error json object
        return error_json_obj


# Download exported bot files into local folder
def download_file(cr_url, download_id, user_token, data_file_path):
    headers = {"X-Authorization": user_token, "accept": "*/*", "accept-encoding": "gzip;deflate;br"}

    log("Download file: no data", 'debug')
    log("Headers: " + str(
        {"X-Authorization": user_token[0:20] + ".******", "accept": "*/*", "accept-encoding": "gzip;deflate;br"}),
        'debug')
    log("URL: " + cr_url + '/v2/blm/download/' + download_id, 'debug')

    response = requests.get(cr_url + '/v2/blm/download/' + download_id, headers=headers)

    # Checking if response status is 200
    if response.status_code == 200:

        with open(data_file_path, 'wb') as output_file:
            output_file.write(response.content)

        # print("File downloaded to: " + str(data_file_path))
        log("File downloaded to: " + str(data_file_path), 'info')

        # Extracting zip file contents
        return "ok"

    else:
        error_json_obj = response.json()

        # print(str(error_json_obj))
        log(str(error_json_obj), 'info')

        # Returning error json object
        return error_json_obj


# Get file details using file path in A360 Control room
def fetch_file_details_by_path(cr_url, user_token, file_path_in_cr):
    data = {
        "path": file_path_in_cr
    }
    headers = {"X-Authorization": user_token, 'Content-type': 'application/json', 'Accept': '*/*'}

    log("Fetch file details by path: " + str(data), 'debug')
    log("Headers: " + str(
        {"X-Authorization": user_token[0:20] + ".******", 'Content-type': 'application/json', 'Accept': 'text/plain'}),
        'debug')
    log("URL: " + cr_url + '/v2/repository/workspaces/public/files/bypath', 'debug')

    response = requests.post(cr_url + '/v2/repository/workspaces/public/files/bypath', json=data, headers=headers)

    # Checking if response status is 200
    if response.status_code == 200:
        json_obj = response.json()

        # print("File ID (" + str(json_obj.get('id')) + ") fetched from control room for file path " + file_path_in_cr)
        log("File ID (" + str(json_obj.get('id')) + ") fetched from control room for file path " + file_path_in_cr,
            'info')

        return json_obj
    else:
        error_json_obj = response.json()

        # print(str(error_json_obj))
        log(str(error_json_obj), 'info')

        # Returning error json object
        return error_json_obj


# Export bot package from A360 Control room
def export_bot_package(args):
    try:
        cr_url = args.get('cr_url')
        user_token = args.get('user_token')
        bot_ids = args.get('bot_ids')
        data_folder_path = args.get('folder_path')

        export_bot_name = "Export." + dt.datetime.today().strftime('%Y%m%d_%H%M%S') + ".py.utility.zip"

        if str(cr_url).endswith("/"):
            cr_url = cr_url[:-1]

        # Get token status
        tok_status = token_status(cr_url, user_token)

        # Checking token status
        if type(tok_status) == str and tok_status == 'false':
            # Returning error
            result = json.dumps({'code': 'user.token.invalid', 'details': '',
                                 'message': 'Given user token is invalid. Please generate a new one.'})
            log(str(result), 'info')
            return result
        elif type(tok_status) == dict:
            # Returning error
            result = json.dumps(tok_status)
            log(str(result), 'info')
            return result

        # Export bot from control room
        request_id = export_bot(cr_url, user_token, export_bot_name, bot_ids)

        # Checking if bot export has started
        if type(request_id) == str and request_id != '':
            download_id = 'wait'

            # Waiting for bot export to be completed
            while type(download_id) == str and download_id == 'wait':
                # Get bot export status
                download_id = bot_export_status(cr_url, request_id, user_token)

            # Checking if bot export is completed
            if type(download_id) == str and download_id != 'wait' and download_id != '':
                # Downloading file
                download_obj = download_file(cr_url, download_id, user_token,
                                             os.path.join(data_folder_path, export_bot_name))

                # Checking if download is success
                if type(download_obj) == str and download_obj == 'ok':
                    # Returning success
                    log(str(export_bot_name), 'error')
                    return export_bot_name
                else:
                    # Returning error
                    result = json.dumps(download_obj)
                    log(str(result), 'error')
                    return result
            else:
                # Returning error
                result = json.dumps(download_id)
                log(str(result), 'error')
                return result
        else:
            # Returning error
            result = json.dumps(request_id)
            log(str(result), 'error')
            return result
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
        #result = json.dumps({'code': 'python.exception', 'details': '', 'message': str(err)})
        log(str(result), 'error')
        return result


# Export and import bots in A360 Control room
def export_import_bot_package(data):
    user_token = generate_token(data['source_cr_url'], data['source_cr_username'], '', data['source_cr_apikey'])

    if type(user_token) == str:

        log("Bot IDs to be exported: " + str(data["bot_ids"]), 'debug')
        bot_ids = data["bot_ids"]
        # file_name = 'Export.20220816_154744.py.utility.zip'
        file_name = export_bot_package(
            {'cr_url': data['source_cr_url'], 'user_token': user_token, 'bot_ids': bot_ids, 'folder_path': os.environ['temp'] + '\\Backups'})

        # print('file_name: ' + file_name)

        log('Check and create folder path (' + os.environ['temp'] + '\\Backups\\' + file_name.replace('.zip',
                                                                                                      '') + ') if not available',
            'debug')

        print(file_name)
        print(file_name.replace('.zip', ''))
        print(os.environ['temp'] + '\\Backups\\' + file_name.replace('.zip', ''))
        Path(os.environ['temp'] + '\\Backups\\' + file_name.replace('.zip', '')).mkdir(parents=True, exist_ok=True)


        if type(user_token) == str:
            user_token = generate_token(data['target_cr_url'], data['target_cr_username'], '', data['target_cr_apikey'])
            return bot_import(data['target_cr_url'], user_token, os.environ['temp'] + '\\Backups',
                              file_name)
        elif type(user_token) == dict:
            result = json.dumps(user_token)
            log(str(result), 'error')
            return result
    elif type(user_token) == dict:
        result = json.dumps(user_token)
        log(str(result), 'error')
        return result

# Function to process the paths
def process_paths(paths):
    result = []
    paths = paths.split(",")
    for path in paths:
        # Modify the path format to replace forward slashes with double backslashes
        modified_path = path.replace('/', '\\')
        # Remove 'bot_' from the directory path if present
        if 'bot_' in modified_path:
            modified_path = modified_path.replace('bot_', '', 1)
        # Check if the path contains "content.json" or "dependencies.json"
        if modified_path.endswith("content.json") or modified_path.endswith("dependencies.json"):
            # Get the directory path
            repository_path = os.path.dirname(modified_path)
            result.append(repository_path)
        else:
            # Return the modified whole path for others
            result.append(modified_path)

    # Remove duplicates by converting the list to a set and back to a list
    unique_result = list(set(result))
    return unique_result

def exportImportBots(data):
    try:
        #data = json.loads(data)


        home_dir = os.path.expanduser("~")
        temp_folder = tempfile.gettempdir()
        # Construct the Desktop folder path
        desktop_path = os.path.join(home_dir, "Desktop")
        log_file_path =  temp_folder + "\\exportImportUtility.log" #data['input_output_folder_path']  + "\\exportImportUtility.log"

        log_level = 'debug'
        initialize_logger(log_file_path=log_file_path, log_level=log_level)
        log(str('helllo'), 'debug')
        log(data['bot_paths'],'debug')



        # if 'cr_url' not in data:
        #     return json.dumps({'code': 'python.exception', 'details': '',
        #                        'message': 'Control room URL is missing, please provide and run the utility again.'})
        # elif 'cr_username' not in data:
        #     return json.dumps({'code': 'python.exception', 'details': '',
        #                        'message': 'Username is missing, please provide it for authentication.'})
        # elif 'cr_password' not in data and 'cr_apikey' not in data:
        #     return json.dumps({'code': 'python.exception', 'details': '',
        #                        'message': 'Both password and apikey are missing, please provide either of them for authentication.'})


        if not os.path.exists(os.environ['temp'] + '\\Backups'):
            os.makedirs(os.environ['temp'] + '\\Backups')

        data['bot_paths'] = process_paths(data['bot_paths'])
        bot_ids = []
        #Get botIds by path
        for item in data['bot_paths']:
            token = generate_token(data['source_cr_url'], data['source_cr_username'], '', data['source_cr_apikey'])
            response= fetch_file_details_by_path(data['source_cr_url'], token,item)
            bot_ids.append(response['id'])

        data["bot_ids"] = bot_ids
        result = export_import_bot_package(data)

        if os.path.exists(os.environ['temp'] + '\\Backups'):
            shutil.rmtree(os.environ['temp'] + '\\Backups', ignore_errors=True)
        return str(result)
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
        return str(result)


SOURCE_CR = {
                'url': 'https://aa-se-ind-5.my.automationanywhere.digital',
                 'username' : 'sikha.creator',
                'apikey' : '@~lyETXFZ<~hT:7PJohku]tpBuU>pRCpO2[yd`Bk'
            }
TARGET_CR = {
                 'url': 'https://aa-saleseng-us-4sbx.cloud.automationanywhere.digital',
                'username' : 'sikha.creator',
                'apikey' : 'G`DWm^r[f=]BKgrZ7}{GL=[uzGC1IJL@A8bXHqjM'
            }



arg1 = sys.argv[1]
exportImportBots( { "source_cr_url": SOURCE_CR['url'], "source_cr_username" :SOURCE_CR['username'], "source_cr_apikey" : SOURCE_CR['apikey'],
               "target_cr_url" :  TARGET_CR['url'], "target_cr_username" :  TARGET_CR['username'], "target_cr_apikey" : TARGET_CR['apikey'],
                "bot_paths" :arg1})