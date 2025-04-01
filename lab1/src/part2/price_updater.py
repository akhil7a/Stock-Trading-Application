from __future__ import print_function

import logging
import time
import random

import grpc
import stock_service_pb2
import stock_service_pb2_grpc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host')

args = parser.parse_args()

host = '127.0.0.1' if args.host == None else args.host
host += ':50018'

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

        print("company",random_company, "price updated to ",random_price)

        function(random_company, random_price)


def run(stock_company, price):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(host) as channel:
        stub = stock_service_pb2_grpc.StockServiceStub(channel)
        updateRes = stub.Update(stock_service_pb2.StockUpdate(stock_name=stock_company, price=price))
        
    # print(updateRes.response)
    if(updateRes.response == 1):
        print('update successful')
    else:
        print("invalid input")


if __name__ == '__main__':
    print("price updater client started...")
    logging.basicConfig()
    run_at_random_times(run, 1, 10)
