import subprocess
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--stock_name')
args = parser.parse_args()

host = '127.0.0.1' if args.host == None else args.host

# taking default stock as GameStart if nothing is passed in arguments
stock_name = 'GameStart' if args.stock_name == None else args.stock_name

for i in range(100):
    # Running as seperate process
    start_time = time.time()
    subprocess.run(["python3", "lookup.py", '--stock_name',stock_name, '--host',host])
    latency = time.time() - start_time
    # print("Request " + str(i) + " latency : " +str(latency) + " seconds")
    print(latency)
