from __future__ import print_function

import logging

import grpc
import stock_service_pb2
import stock_service_pb2_grpc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--stock_name')
args = parser.parse_args()

host = '127.0.0.1' if args.host == None else args.host
host += ':50018'

# taking default stock as GameStart if nothing is passed in arguments
stock_name = 'GameStart' if args.stock_name == None else args.stock_name

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    # print("lookup client started...")
    with grpc.insecure_channel(host) as channel:
        stub = stock_service_pb2_grpc.StockServiceStub(channel)
        lookup_result = stub.Lookup(stock_service_pb2.StockCompany(stock_name=stock_name))
        
    if(lookup_result.price == -1):
        print("invalid stock given")
    else:
        print("price of",stock_name,"is trading with",round(lookup_result.price,2),"in volume of",lookup_result.trading_volume)
    # print(lookup_result.price, lookup_result.trading_volume)

    
if __name__ == '__main__':
    logging.basicConfig()
    run()
