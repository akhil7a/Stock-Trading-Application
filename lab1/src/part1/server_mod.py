import socket
import threading
import queue
import time

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

class ThreadPool:
    def __init__(self, num_threads):
        self.task_queue = queue.Queue()
        self.threads = []
        self.lock = threading.Lock()
        for i in range(num_threads):
            thread = threading.Thread(target=self.worker)
            self.threads.append(thread)
            thread.start()
    
    def add_task(self, task):
        # with self.lock:
        self.task_queue.put(task)
    
    def worker(self):
        while True:
            self.lock.acquire()
            task = self.task_queue.get()
            if task is None:
                break
            self.lock.release()
            task()
            # self.task_queue.task_done()

class SocketServer:
    def __init__(self, host, port, num_threads):
        self.host = host
        self.port = port
        self.threadpool = ThreadPool(num_threads)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
    
    def serve_forever(self):
        # print(f'Starting server on {self.host}:{self.port}...')
        while True:
            client_socket, address = self.server_socket.accept()
            print(f'Accepted connection from {address}')
            self.threadpool.add_task(lambda: self.handle_client(client_socket, address))
    
    def handle_client(self, client_socket, address):
        # with client_socket:
            # while True:
        print("address in handle ", address, client_socket)
        data = client_socket.recv(1024)
        if not data:
            print("no data")
            # break
        print(f'Received data: {data.decode()}')
        # response = f'Response to {data.decode()}'.encode()
        stock_price = Lookup(data.decode())
        client_socket.sendall(stock_price.encode())
        print('Closing connection')

    def shutdown(self):
        self.server_socket.close()
        for i in range(len(self.threadpool.threads)):
            self.threadpool.add_task(None)
        for thread in self.threadpool.threads:
            thread.join()

socket = SocketServer('127.0.0.1', 1197, 1)
socket.serve_forever()

