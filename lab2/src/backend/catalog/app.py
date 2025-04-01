from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor
from service import lookup, is_trade_valid, catalog
import time
import threading

# initializing the threadpool
pool = ThreadPoolExecutor(max_workers=10)

exit_flag = False

# Define a function called update_db that writes the contents of the in-memory 
# catalog to a JSON file every 20 seconds
def update_db():
    while not exit_flag:
        # Wait for 20 seconds
        time.sleep(20)
        # Open the db.json file in write mode and dump the catalog into it as a JSON object
        with open('db.json', 'w') as file:
            json.dump(catalog, file)
    
    return

# defining a class that inherits the BaseHTTPRequestHandler
class CatalogHandler(BaseHTTPRequestHandler):
    # method to handle all the GET methods
    def do_GET(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        # Check if the path starts with '/catalog'
        if parsed_path.path.startswith('/catalog/'):
            # Extract the stock name from the URL path
            stock_name = parsed_path.path.split('/')[-1]
            # Submit a lookup task to the thread pool
            future = pool.submit(lookup, stock_name)
            # Wait for the lookup task to complete and get the result
            result = future.result()
            if(result != None):
                # If the result is not None, create a response object and add the result to it
                response = {}
                # iterating over the result to keep only the values needed
                for key in result.keys():
                    if key != 'trading_volume':
                        response[key] = result[key]
                print('lookup result: ', response)
                # Send a success response to the client with body as response dictionary
                self.handle_response(200, response)
                return
            else:
                # If the result is None, send a 404 error response to the client
                self.error_handler(404, 'Stock Not Found!')
        else:
            # If the URL path does not start with '/catalog/', send a 404 error response to the client
            self.error_handler(404, 'Path Not Found!')

    # method to handle all the PUT methods
    def do_PUT(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        # Check if the path starts with '/catalog'
        if parsed_path.path.startswith('/catalog'):
            # Read the content length of the request body
            content_length = int(self.headers.get('Content-Length', 0))
            # Read the payload from the request body and deserialize from JSON
            payload = self.rfile.read(content_length).decode('utf-8')
            payload = json.loads(payload)
            # Submit the is trade valid task to a thread pool to lookup the stock information
            # and update the catalog information with appropriate logic
            future = pool.submit(is_trade_valid, payload)
            # Wait for the result from the thread pool
            result, error = future.result()
            # If the result is not None, send the 200 ok response
            if(result != None):
                self.handle_response(200, result)
                print('response for a request from oder microservice: ', result)
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
    server_address = ('', 8088)
    print('Starting server at %s:%d' % server_address)
    # create an HTTP server with CatalogHandler
    httpd = HTTPServer(server_address, CatalogHandler)
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
        print("writing db file....")
        exit_flag = True
        # wait for the thread to finish before moving to next step
        t.join()
        # write the contents of the catalog to the db.json file
        with open('db.json', 'w') as file:
            json.dump(catalog, file)
        
        print("done writing to the file!!")
        print("shutting down the server...")
        httpd.shutdown()