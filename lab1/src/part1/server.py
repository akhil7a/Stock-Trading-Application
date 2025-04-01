import socket
import time
from ThreadPool import ThreadPool
# import queue
# import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--num_threads')
args = parser.parse_args()

no_of_threads = 1 if args.num_threads == None else args.num_threads

# stock info dictionary
stock_info = {
    "GameStart": {
        "price": 20,
        "trading_volume": 0
    },
    "FishCo": {
        "price": 100,
        "trading_volume": 0
    }
}

# method to lookup company and return price if found
def Lookup(stock_company):
    time.sleep(3)
    if(stock_info.get(stock_company) != None):
        price = str(stock_info.get(stock_company).get('price'))
    else:
        price = '-1'
    
    return price

# method to handle client requests
def handle_client_request(client_socket):
    print("client_docket in handle ", client_socket, time.time())
    
    stock_company = client_socket.recv(1024).decode()

    stock_price = Lookup(stock_company)
    # time.sleep(3)
    client_socket.send(stock_price.encode())

    client_socket.close()

sock = socket.socket()
host = "127.0.0.1"
print(host)
port = 1198
sock.bind((host, port))

# initialising a pool of threads
threadpool = ThreadPool(no_of_threads)

sock.listen(5)

while True:
    client_socket, client_address = sock.accept()
    print("client_docket in main ", client_socket, time.time())
    # time.sleep(0.1)
    # creating lambda function to pass socket context into the task queue
    client_task = lambda: handle_client_request(client_socket)
    threadpool.push_task(client_task)
    # threadpool.submit_task(client_task)