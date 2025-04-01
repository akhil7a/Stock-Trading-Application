from concurrent import futures
import logging

import grpc
import stock_service_pb2
import stock_service_pb2_grpc

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--num_threads')
parser.add_argument('--gamestart_vol')
parser.add_argument('--fishco_vol')
parser.add_argument('--boarco_vol')
parser.add_argument('--menhirco_vol')
args = parser.parse_args()

# taking default stock as GameStart if nothing is passed in arguments
num_threads = 2 if args.num_threads == None else int(args.num_threads)


# stock lookup dictionary
stock_info = {
    "GameStart": {
        "price": 20,
        "trading_vol": 0,
        "max_vol":100 # make it configurable during run-time
    },
    "FishCo": {
        "price": 100,
        "trading_vol": 0,
        "max_vol":50 # make it configurable during run-time
    },
    "BoarCo": {
        "price": 150,
        "trading_vol": 0,
        "max_vol":200 # make it configurable during run-time
    },
    "MenhirCo": {
        "price": 120,
        "trading_vol": 0,
        "max_vol":150 # make it configurable during run-time
    }
}

gamestart_info = stock_info['GameStart']
fishco_info = stock_info['FishCo']
boarco_info = stock_info['BoarCo']
menhirco_info = stock_info['MenhirCo']

gamestart_info['max_vol'] = 100 if args.gamestart_vol == None else int(args.gamestart_vol)
fishco_info['max_vol'] = 100 if args.fishco_vol == None else int(args.fishco_vol)
boarco_info['max_vol'] = 100 if args.boarco_vol == None else int(args.boarco_vol)
menhirco_info['max_vol'] = 100 if args.menhirco_vol == None else int(args.menhirco_vol)


# get lookup info function
def get_stock_info(company):
    if(stock_info.get(company) != None):
        companyData = stock_info.get(company)
        price = companyData.get('price')
        trading_vol = companyData.get('trading_vol')
        resp = {
            'price': price,
            'trading_vol': trading_vol
        }
    else:
        resp = {
            'price': -1
        }
    
    return resp


# method to update trading volume.
def do_stock_trading(company, trading_volume, trading_type):

    if(stock_info.get(company) != None):
        companyData = stock_info.get(company)
        trading_vol = companyData.get('trading_vol')
        max_vol = companyData.get('max_vol')
        if(trading_vol > max_vol):
            return 0
        companyData['trading_vol'] = trading_vol + trading_volume

        return 1
    else:
        return -1


# method to update the price of the stock randomly from client side
def update_price(company, price):
    if(price < 0):
        return -2
    else:
        if(stock_info.get(company) != None):
            companyData = stock_info.get(company)
            companyData['price'] = round(price, 2)
            return 1
        else:
            return -1


class StockServicer(stock_service_pb2_grpc.StockServiceServicer):

    # lookup rpc method definition
    def Lookup(self, request, context):
        stock_info = get_stock_info(request.stock_name)
        return stock_service_pb2.StockInfo(price=stock_info.get('price'), trading_volume=stock_info.get('trading_vol'))
    
    # trade rpc method defintion
    def Trade(self, request, context):
        trading_result = do_stock_trading(request.stock_name, request.trading_volume, request.type)
        return stock_service_pb2.TradingResponse(response=trading_result)

    # update price method definition
    def Update(self, request, context):
        update_result = update_price(request.stock_name, request.price)
        return stock_service_pb2.UpdateResponse(response=update_result)


# initialize the server to serve gRPC methods
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=num_threads))
    stock_service_pb2_grpc.add_StockServiceServicer_to_server(
        StockServicer(), server)
    server.add_insecure_port('[::]:50018')
    server.start()
    print("Server started, listening on ", 50018)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
