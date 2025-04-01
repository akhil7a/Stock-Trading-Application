import socket
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--port')
parser.add_argument('--stock_name')
args = parser.parse_args()

host = '127.0.0.1' if args.host == None else args.host
port = 1234 if args.port == None else int(args.port)

# taking default stock as GameStart if nothing is passed in arguments
stock_name = 'GameStart' if args.stock_name == None else args.stock_name

start_time = time.time()

#create socket object
socket_connection = socket.socket()

# connection to server established
socket_connection.connect((host, port))

client_arguments=[]

function_name='lookup'

# Appending command line arguments input to a list
client_arguments.append(function_name)
client_arguments.append(stock_name)

# Converting client_arguments to string from list
client_arguments=str(client_arguments)

# send stock name and function name as input from client to server through socket
socket_connection.send(client_arguments.encode())

# recieve stock price as output from server to client through socket
recieved_response = socket_connection.recv(1024).decode() 

if int(recieved_response) == -1:
    print("Stockname is not found in the market")
else:
    print("Stock price of",stock_name,"is",recieved_response)

# Close the socket when done
socket_connection.close()
