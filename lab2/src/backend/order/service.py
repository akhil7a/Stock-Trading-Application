import threading
import requests
import os
import json

# initializing the locks
read_lock = threading.Lock()
write_lock = threading.Lock()

# on server start reading the log.json file and loading its contents to in-memory transaction history data
with open('log.json', 'r') as file:
    data = file.read()

transaction_history = json.loads(data)

# initializing the transaction number to -1 as we have to send transaction number starting with 0
transaction_number = -1

# reading environment variables to extract ip address of catalog service
catalog_host = os.getenv("CATALOG_HOST", "catalog")
print('catalog_host: ', catalog_host)

# if the transaction histoy is already found, we are updating the transaction number with 
# the transaction number of the last record in the db
if len(transaction_history) != 0:
    transaction_number = transaction_history[-1]['transaction_number']

# method to call the catalog microservice API
def request(payload):
    # constructing the URL
    url = 'http://'+catalog_host+':8088/catalog'
    # setting headers to support json request payload
    headers = {
        'Content-Type': 'application/json'
    }
    # calling PUT method of catalog service with requests module with json payload
    response = requests.put(url, json=payload, headers=headers)
    return response

# function to handle the request and update the transaction information accordingly
def handle_request(payload):
    global transaction_number
    # calling catalog api to lookup stock info and update the stock info in the catalog microservice
    catalog_response = request(payload)
    # decoding the response into JSON format and deserializing the response
    result = json.loads(catalog_response.content.decode('utf-8'))

    # checking for the response status code
    if catalog_response.status_code == 200:
        # acquiring the write lock
        with write_lock:
            # incrementing the transaction number
            transaction_number += 1
            # deleting the price from result as it is not required
            del result['price']
            # adding additional required fields to the the result object
            result['type'] = payload['type']
            result['transaction_number'] = transaction_number
            # adding the result object at the end of the transaction history list
            transaction_history.append(result)
        # returning success and None as error
        return 'success', None
    else:
        print("Error:", catalog_response.content.decode('utf-8'))
        # reading the error code from response status code
        code = catalog_response.status_code
        # returning None as success and error object in a structured format as error
        return None, {'code': code, 'error': result['error']}