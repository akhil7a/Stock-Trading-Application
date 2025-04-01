import threading
import socket
import queue
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--num_threads')
parser.add_argument('--host')
parser.add_argument('--port')
args = parser.parse_args()

number_of_threads = 2 if args.num_threads == None else int(args.num_threads)
host = '127.0.0.1' if args.host == None else args.host
port = 1234 if args.port == None else int(args.port)

print('number_of_threads =',number_of_threads)

# create socket object
socket_connection = socket.socket()
socket_connection.bind((host, port))
socket_connection.listen(5)

print("Server started on ",host,":",port)

thread_pool_list=[]
task_queue=queue.Queue()

# Dictionary for Stock names
stock_info = {
    "GameStart": {
        "price": 20,
        "tradingVol": 0
    },
    "FishCo": {
        "price": 100,
        "tradingVol": 0
    }
}

# function to lookup company names and return their prices if found
def lookup(stock_company_name):
    if(stock_info.get(stock_company_name) != None):
        stock_price = str(stock_info.get(stock_company_name).get('price'))
    else:
        stock_price = "-1"

    return stock_price

# function to check semantics of client input and perform actions accordingly
def check_task_queue():
    while True:
        try:
            client_socket = task_queue.get(timeout=0.1)
            client_arguments = client_socket.recv(1024).decode()

            # Converting string to list back again
            client_arguments=eval(client_arguments)
            function_name=client_arguments[0]
            stock_company_name=client_arguments[1]
        
            if function_name=='lookup':
                result = lookup(stock_company_name)
                client_socket.send(result.encode())
            else:
                client_socket.send('Wrong Input'.encode())
            client_socket.close()
        except queue.Empty:
            pass

# Loop to create Thread Pool
for i in range(number_of_threads):
    thread = threading.Thread(target=check_task_queue)
    thread.start()
    thread_pool_list.append(thread)

while True:
    client_socket, client_address = socket_connection.accept()

    # Put client_socket from client to task_queue
    task_queue.put(client_socket)