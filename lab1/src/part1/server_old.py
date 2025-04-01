import threading
import socket
import queue
import time

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


class ThreadPool:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.threads = []
        self.running = True

        # Create worker threads
        for i in range(num_threads):
            t = threading.Thread(target=self._worker_thread)
            t.start()
            self.threads.append(t)

    def _worker_thread(self):
        while self.running:
            try:
                # print(self.threads)
                queueTask = self.task_queue.get()

                queueTask()
            except queue.Empty:
                pass

    def submit_task(self, task):
        self.task_queue.put(task)

    def shutdown(self):
        self.running = False

        for t in self.threads:
            t.join()

def lookup(stock_company_name):
    if(stock_info.get(stock_company_name) != None):
        stock_price = str(stock_info.get(stock_company_name).get('price'))
    else:
        stock_price = "-1"
    return stock_price

# create socket object
socket_connection = socket.socket()
host = "127.0.0.1"
port = 1261

socket_connection.bind((host, port))

pool = ThreadPool(1)

socket_connection.listen(5)

def handle_client_data(client_socket):
    print("client_socket in handle ", client_socket)
    
    stock_company_name = client_socket.recv(1024).decode()

    result = lookup(stock_company_name)
    # time.sleep(3)
    client_socket.send(result.encode())

    client_socket.close()

while True:
    client_socket, client_address = socket_connection.accept()
    print("client_socket in main ", client_socket)
    task = lambda: handle_client_data(client_socket)
    pool.submit_task(task)