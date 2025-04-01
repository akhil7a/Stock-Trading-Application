from __future__ import print_function

import logging
import time
import random

import grpc
import stock_service_pb2
import stock_service_pb2_grpc

# define stock price ranges to update randomly in the range
stocks = {
    'GameStart': [10,100],
    'FishCo': [30, 90],
    'BoarCo': [20, 80],
    'MenhirCo': [50, 150]
}

def run_at_random_times(function, min_delay, max_delay):
    while True:
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        companys = ['GameStart', 'FishCo', 'BoarCo', 'MenhirCo']
        random_index = random.randint(0,3)
        random_company = companys[random_index]

        price_range = stocks.get(random_company)
        random_price = round(random.uniform(price_range[0], price_range[1]), 2)

        print(random_company, random_price)

        function(random_company, random_price)


def run(stock_company, price):
    print(price)
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("client started...")
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        stub = stock_service_pb2_grpc.StockServiceStub(channel)
        updateRes = stub.Update(stock_service_pb2.StockUpdate(stock_name=stock_company, price=price))

    print(updateRes.response)


if __name__ == '__main__':
    logging.basicConfig()
    run_at_random_times(run, 1, 10)
