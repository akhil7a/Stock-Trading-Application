from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor
from service import handle_request, transaction_history
import time
import threading

# initializing the threadpool
pool = ThreadPoolExecutor(max_workers=10)

exit_flag = False

# Define a function called update_db that writes the contents of the in-memory 
# transaction to a JSON file every 20 seconds
def update_db():
    while not exit_flag:
        # Wait for 20 seconds
        time.sleep(20)
        # Open the log.json file in write mode and dump the transaction into it as a JSON object
        with open('log.json', 'w') as file:
            json.dump(transaction_history, file)
    return

# defining a class that inherits the BaseHTTPRequestHandler
class OrderHandler(BaseHTTPRequestHandler):
    # method to handle all the POST methods
    def do_POST(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        # Check if the path starts with '/orders'
        if parsed_path.path.startswith('/orders'):
            # Read the content length of the request body
            content_length = int(self.headers.get('Content-Length', 0))
            # Read the payload from the request body and deserialize from JSON
            payload = self.rfile.read(content_length).decode('utf-8')
            payload = json.loads(payload)
            # Submit the handle reqeust task to a thread pool to lookup the stock information
            # and update the transaction information with appropriate logic
            future = pool.submit(handle_request, payload)
            # Wait for the result from the thread pool
            result, error = future.result()
            # If the result is not None, send the 200 ok response by adding transaction_number
            if(result != None):
                response = {'transaction_number': transaction_history[-1]['transaction_number']}
                print("trade response: ", response)
                self.handle_response(200, response)
                return
            # If the error is not None, handle the error by sending the code and appropriate error
            else:
                self.error_handler(error['code'], error['error'])

    # function to handle the error responses
    def error_handler(self, code, message):
        # Create an empty dictionary called "response"
        response = {}
        # Set the values of "error" keys in the "response" dictionary
        response['error'] = message
        print('error response: ', response)
        # send the error response back to the client
        self.handle_response(code, response)
        return
    
    # function to send responses to the client with status code and response body
    def handle_response(self, code, response):
        # set HTTP response code
        self.send_response(code)
        # set response content type to JSON
        self.send_header('Content-type', 'application/json')
        # end response headers
        self.end_headers()
        # encode the response object as JSON and write it to the response body (serialization)
        self.wfile.write(json.dumps(response).encode())
        return

if __name__ == '__main__':
    # set up server address
    server_address = ('', 8089)
    print('server listening')
    # create an HTTP server with OrderHandler
    httpd = HTTPServer(server_address, OrderHandler)
    # create a thread to update the database periodcally every 5 seconds
    # submitting it to the thread because to avoid blocking the main thread
    t = threading.Thread(target=update_db)
    t.start()
    
    try:
        # start serving requests
        httpd.serve_forever()
    except KeyboardInterrupt:
        # catch KeyboardInterrupt and initiate shutdown process
        print("shutdown called...")
        print("writing log file....")
        exit_flag = True
        # wait for the thread to finish before moving to next step
        t.join()
        # write the contents of the transaction hisotry to the log.json file
        with open('log.json', 'w') as file:
            json.dump(transaction_history, file)
        
        print("done writing to the file!!")
        print("shutting down the server...")
        httpd.shutdown()