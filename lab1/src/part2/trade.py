from __future__ import print_function

import logging

import grpc
import stock_service_pb2
import stock_service_pb2_grpc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--stock_name')
parser.add_argument('--trading_volume')
parser.add_argument('--trading_type')
args = parser.parse_args()

host = '127.0.0.1' if args.host == None else args.host
host += ':50018'

# taking default stock as GameStart if nothing is passed in arguments
stock_name = 'GameStart' if args.stock_name == None else args.stock_name
# default value of trading volume is 10 if nothing is passed
trading_volume = 10 if args.trading_volume == None else int(args.trading_volume)
# checking for valid volume
if(trading_volume < 0):
    print("invalid trading volume")
    exit()
# default value of trading type is BUY if nothing is passed
trading_type = 'BUY' if args.trading_type == None else args.trading_type
# checking for invalid trading type
if(trading_type != "BUY" and trading_type != "SELL"):
    print("invalid trading type")
    exit()

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    # print("trade client started...")
    with grpc.insecure_channel(host) as channel:
        stub = stock_service_pb2_grpc.StockServiceStub(channel)
        tradingRes = stub.Trade(stock_service_pb2.TradingInfo(stock_name=stock_name, trading_volume=trading_volume, type=trading_type))
        
    # print(tradingRes.response)
    if(tradingRes.response == 1):
        print('operation success')
    elif(tradingRes.response == 0):
        print('Trading suspended')
    elif(tradingRes.response == -1):
        print('invalid stock given')
    
if __name__ == '__main__':
    logging.basicConfig()
    run()
