from __future__ import print_function

import logging

import grpc
import stock_service_pb2
import stock_service_pb2_grpc
import time

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    # print("client started...")
    start_time = time.perf_counter()
    # for i in range(10):
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        stub = stock_service_pb2_grpc.StockServiceStub(channel)
        lookupRes = stub.Lookup(stock_service_pb2.StockCompany(stock_name='FishCo'))

        end_time = time.perf_counter()
        print(end_time - start_time)
        # tradingRes = stub.Trade(stock_service_pb2.TradingInfo(stock_name='FishCo', trading_volume=10, type='BUY'))
        
    print(round(lookupRes.price, 2), lookupRes.trading_volume)
    # print(tradingRes.response)
    


if __name__ == '__main__':
    logging.basicConfig()
    run()
