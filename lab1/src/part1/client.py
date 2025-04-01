#!/usr/bin/env python3
import socket
import argparse
import time

# parser = argparse.ArgumentParser()
# parser.add_argument('--host')
# parser.add_argument('--port')
# parser.add_argument('--stock')
# args = parser.parse_args()

# host = socket.gethostname()  # Get local machine name

host = '127.0.0.1' #if args.host == None else args.host
port = 1197 #if args.port == None else args.port
# taking default stock as GameStart if nothing is passed in arguments
stock_name = 'GameStart' #if args.stock == None else args.stock

# for i in range(2):
# start_time = time.perf_counter()
client_socket = socket.socket()


client_socket.connect((host, port))
print("client socket ", client_socket)
client_socket.send(stock_name.encode())
server_data = client_socket.recv(1024).decode()
# latency = time.perf_counter() - start_time
# print(" latency : " +str(latency) + " seconds")
if(int(server_data) == -1):
    print('given stock not found, received -1 from server')
else:
    print(stock_name,"price is", server_data)
client_socket.close()
