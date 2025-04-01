from concurrent import futures
import logging

import grpc
import stock_service_pb2
import stock_service_pb2_grpc
from threading import Lock
import time

stockLookupInfo = {
    "GameStart": {
        "price": 20,
        "tradingVol": 0,
        "maxVol":100 # make it configurable during run-time
    },
    "FishCo": {
        "price": 100,
        "tradingVol": 0,
        "maxVol":50 # make it configurable during run-time
    },
    "BoarCo": {
        "price": 150,
        "tradingVol": 0,
        "maxVol":200 # make it configurable during run-time
    },
    "MenhirCo": {
        "price": 120,
        "tradingVol": 0,
        "maxVol":150 # make it configurable during run-time
    }
}

def get_stock_info(company):
    #lock
    if(stockLookupInfo.get(company) != None):
        companyData = stockLookupInfo.get(company)
        price = companyData.get('price')
        tradingVol = companyData.get('tradingVol')
        resp = {
            'price': price,
            'tradingVol': tradingVol
        }
    else:
        resp = {
            'price': -1
        }
    #unlock
    time.sleep(0.1)
    return resp

"""
What is the use of trading_type here????
"""
def do_stock_trading(company, trading_volume, trading_type):
    if(stockLookupInfo.get(company) != None):
        companyData = stockLookupInfo.get(company)
        tradingVol = companyData.get('tradingVol')
        maxVol = companyData.get('maxVol')
        if(tradingVol > maxVol):
            return 0
        companyData['tradingVol'] = tradingVol + trading_volume
        return 1
    else:
        return -1


"""
think of more invalid prices
"""
def update_price(company, price):
    print("price in server", price, round(price, 2))
    if(price < 0):
        return -2
    else:
        if(stockLookupInfo.get(company) != None):
            companyData = stockLookupInfo.get(company)
            companyData['price'] = round(price, 2)
            print(companyData['price'])
            return 1
        else:
            return -1


class StockServicer(stock_service_pb2_grpc.StockServiceServicer):

    # lookup rpc method definition
    def Lookup(self, request, context):
        #lock
        stock_info = get_stock_info(request.stock_name)
        #unlock
        return stock_service_pb2.StockInfo(price=stock_info.get('price'), trading_volume=stock_info.get('tradingVol'))
    
    # trade rpc method defintion
    def Trade(self, request, context):
        # lock = Lock()
        # lock.acquire()
        trading_result = do_stock_trading(request.stock_name, request.trading_volume, request.type)
        # lock.release()
        return stock_service_pb2.TradingResponse(response=trading_result)

    # update price method definition
    def Update(self, request, context):
        update_result = update_price(request.stock_name, request.price)
        return stock_service_pb2.UpdateResponse(response=update_result)

# initialize the server to serve gRPC methods
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stock_service_pb2_grpc.add_StockServiceServicer_to_server(
        StockServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on ", 50051)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
