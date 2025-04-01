import random
import time
import requests
import json
import argparse

# defining stocks list to randomly pick one stock from the list
stocks = ["GameStart", "FishCo", "MenhirCo", "BoarCo"]

# Parser to extract the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--probability')
args = parser.parse_args()

# Read the probability from command line arguments and set the probability "p" for sending another order request
p = 0.5 if args.probability == None else float(args.probability)

# initiating session object using requests module
session = requests.Session()
# setting a flag to check if a session is closed or not
is_session_closed = False

# variables to maintain all the aggregate latencies (part3)
lookup_sum = 0
trade_sum = 0

# method to pick a random stock from the stocks list
def pick_random_stock():
    # pick a random stock
    stock = random.choice(stocks)
    return stock

while True:
# for i in range(100):

    if is_session_closed:
        session = requests.Session()
        is_session_closed = False

    # pick a random stock
    stock_name = pick_random_stock()

    # tracking time to calculate latency (part3)
    start_time = time.time()
    # calling the lookup method with the previous session created
    response = session.get('http://localhost:3010/catalog/' + stock_name)

    # calculating the latency (part3)
    lookup_latency = time.time() - start_time

    # aggregating the latency sum (part3)
    lookup_sum += lookup_latency

    # decoding the response into JSON format and deserializing the response
    response_data = json.loads(response.content.decode('utf-8'))
    print('response_data: ', response_data)
    # time.sleep(3)

    # checking for the positive quantity
    if response_data["data"]["quantity"] > 0:
        # Randomly decide whether to send another order request based on probability "p"
        if random.random() < p:
            # construct the payload object for order request with required fields
            payload = {
                'name': stock_name,
                'type': 'sell', #random.choice(['sell', 'buy']),
                'quantity': random.randint(1, 100)
            }
            # add content-type as json in headers
            headers = {
                'Content-Type': 'application/json'
            }

            # tracking time to calculate latency (part3)
            start_time = time.time()

            # Send another order request using the same HTTP connection (same session)
            order_response = session.post('http://localhost:3010/orders', json=payload, headers=headers)
            
            # calculating the latency (part3)
            trade_latency = time.time() - start_time

            # calculating the aggregate latency sum
            trade_sum += trade_latency

            # decoding the response into JSON format and deserializing the response
            order_response_data = json.loads(order_response.content.decode('utf-8'))
            print('order_response_data: ', order_response_data)
            if order_response.status_code != 200:
                print(order_response_data)
    else:
        print("session closed")
        is_session_closed = True
        session.close()

# print("lookup latencies: ")
# print('lookup_sum: ', lookup_sum)

# print("trade latencies: ")
# print('trade_sum: ', trade_sum)