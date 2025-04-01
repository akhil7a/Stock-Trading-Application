from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import json
import requests
import os

# environment variable to read ip of the catalog server
catalog_host = os.getenv("CATALOG_HOST", "catalog")

#environment variable to read ip of the order server
order_host = os.getenv("ORDER_HOST", "order")

# function to make an API request to server using requests module with passed HTTP method, 
# url and payload if any
def request(method, url, payload=None):
    # setting headers to support json request payload
    headers = {
        'Content-Type': 'application/json'
    }
    # using requests module to call the server with method, url, headers and payload if any as 
    # parameters
    if payload is None:
        response = requests.request(method=method, url=url, headers=headers)
    else:
        response = requests.request(method=method, url=url, headers=headers, json=payload)
    
    # returning the response received from the server
    return response

# function to make API calls to catalog microservice and order microservice with given 
# path, payload
def handle(service_name, path, payload=None):

    # checking for the service name and calling the corresponding microservice for lookup
    # and trade requests
    if service_name == 'catalog':
        method = 'GET'
        # constructing the url
        url = 'http://'+catalog_host+':8088' + path
    elif service_name == 'orders':
        method = 'POST'
        # constructing the url
        url = 'http://'+order_host+':8089' + path
    else:
        return None
    
    # calling the request function with HTTP method and HTTP URL to get the HTTP response
    response = request(method=method, url=url, payload=payload)
    # decoding the response into JSON format and deserializing the response
    result = json.loads(response.content.decode('utf-8'))
    # if response status code is 200, return success response and error as None
    # else if response status code is not 200, return success as None and error object received
    # from the server
    if response.status_code == 200:
        return result, None
    else:
        return None, {'code': response.status_code, 'error': result['error']}

class RequestHandler(BaseHTTPRequestHandler):
    
    # handling HTTP GET methods in this function
    def do_GET(self):
        # extracting the path from the URL
        path = self.path
        # calling the catalog microservice by passing the respective path
        result, error = handle('catalog', path=path)
        # if response is success, return 200 success response by adding the top level data object
        # to the response and sending it to the client
        # else if we get error, return 4XX error response by adding the top level error object
        # to the error response and sending it to the client
        if result != None:
            self.handle_response(200, result)
            return
        else:
            self.error_handler(error['code'], error['error'])
            return

    # handling HTTP POST methods in this function
    def do_POST(self):
        # extracting the path from the URL
        path = self.path
        # extracting the Content-Length value from the headers if it is present, else taking it as 0
        content_length = int(self.headers.get('Content-Length', 0))
        # Read the request payload from the incoming HTTP request
        payload = self.rfile.read(content_length).decode('utf-8')
        # Parse the payload as a JSON object
        payload = json.loads(payload)
        # calling the order microservice with respective path and JSON payload to the server
        result, error = handle('orders', path=path, payload=payload)
        # if response is success, return 200 success response by adding the top level data object
        # to the response and sending it to the client
        # else if we get error, return 4XX error response by adding the top level error object
        # to the error response and sending it to the client
        if result != None:
            self.handle_response(200, result)
            return
        else:
            self.error_handler(error['code'], error['error'])
    
    # function to handle the error responses
    def error_handler(self, code, message):
        # Create an empty dictionary called "error"
        error = {}
        # Set the values of the "code" and "message" keys in the "error" dictionary
        error['code'] = code
        error['message'] = message
        # Create a dictionary called "response" and set the value of the "error" key to the "error" dictionary
        # adding top-level error object to the error response
        response = {}
        response['error'] = error
        # sending the response to the client with HTTP status code and response.
        self.handle_response(code, response, error=True)
        return
    
    # function to send responses to the client with status code and response body
    def handle_response(self, code, result, error=False):
        # Send an HTTP response with the given HTTP status code
        self.send_response(code)
        # if we are handling the error response, we are just converting the result to the response
        # if we are handling 200 success response, we are adding the top-level data object to the response
        # set response to a JSON-encoded version of the "result" object.
        if not error:
            data = {}
            data['data'] = result
            response = json.dumps(data).encode()
        else:
            response = json.dumps(result).encode()
        # Send an HTTP header indicating that the response is in JSON format
        self.send_header('Content-type', 'application/json')
        # Send an HTTP header indicating the length of the response content
        self.send_header("Content-Length", str(len(response)))
        # End the HTTP headers section
        self.end_headers()
        # Write the response content to the response stream
        self.wfile.write(response)
        return
    
# Define a subclass of the built-in HTTPServer class that supports threading
class ThreadedHTTPServer(HTTPServer):
    
    # Define a constructor that calls the superclass constructor and initializes some instance variables
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        # intitalizing the lock
        self.lock = threading.Lock()
        self.threads = []

    # Override the process_request method to spawn a new thread for each incoming request
    def process_request(self, request, client_address):
        # Create a new thread to handle the request using the handle_request method
        t = threading.Thread(target=self.handle_request, args=(request, client_address))
        # Acquire the lock to ensure thread-safe access to the threads list
        self.lock.acquire()
        # Add the new thread to the list of threads
        self.threads.append(t)
        # Release the lock to allow other threads to access the threads list
        self.lock.release()
        # Start the new thread
        t.start()
    
    # method that delegates the request handling to the RequestHandler class
    def handle_request(self, request, client_address):
        # time.sleep(2)
        self.RequestHandlerClass(request, client_address, self)
    
    # method to wait for all spawned threads to finish before exiting the program
    def process_exit(self):
        for t in self.threads:
            t.join()

# If the script is executed as the main program, create a new instance of the ThreadedHTTPServer class
# and start serving HTTP requests forever until a KeyboardInterrupt is raised or the program is terminated.
if __name__ == '__main__':
    server_address = ('', 3010)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    print('Starting server at %s:%d' % server_address)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.process_exit()