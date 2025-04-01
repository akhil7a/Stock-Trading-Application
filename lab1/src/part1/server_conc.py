import socket
import concurrent.futures
import time

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
    # time.sleep(3)
    if(stock_info.get(stock_company) != None):
        price = str(stock_info.get(stock_company).get('price'))
    else:
        price = '-1'
    
    return price

class ThreadPoolTCPServer:
    def __init__(self, num_threads, host, port):
        self.num_threads = num_threads
        self.host = host
        self.port = port
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()

    def serve_forever(self):
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                conn, addr = self.socket.accept()
                self.executor.submit(self.handle_client, conn, addr)
        finally:
            self.shutdown()

    def handle_client(self, conn, addr):
        with conn:
            print(f"New client connected from {addr}")
            while True:
                stock_company = conn.recv(1024).decode()
                if not stock_company:
                    break
                # conn.sendall(data)
                stock_price = Lookup(stock_company)
                # time.sleep(3)
                conn.send(stock_price.encode())
            print(f"Client from {addr} disconnected")

    def shutdown(self):
        self.executor.shutdown(wait=True)
        self.socket.close()

sock = ThreadPoolTCPServer(2, '127.0.0.1', 1197)
sock.serve_forever()
sock.handle_client()

