Commands to run the server and clients.

## Part1:
    Server:
        python3 server.py
            Options:
                --host (optional, default is 127.0.0.1)
                    server host name 
                --port (optional, default is 1234)
                    server port
                --num_threads (optional, default is 2)
                    number of threads in the threadpool
            Example:
                python3 server.py --host=elnux7.cs.umass.edu --port=1100 --num_threads=3

    Client: In part1, we have 2 client files and 1 shell script.
        client.py: (Just sends a 1 request to the server to lookup the stock info)
            python3 client.py
                Options:
                    --host (optional, default is 127.0.0.1)
                        server host name
                    --port (optional, default is 1234)
                        server port
                    --stock_name (optional, default is GameStart)
                        stock name to lookup in the server
                    
                Example: 
                    python3 client.py --host=elnux7.cs.umass.edu --port=1100 --stock_name=FishCo

        client_runner.py: (To run the above client program multiple times with sequential requests which is configurable and measures the latency for every request. Currently 100 requests are configured inside the code. we can change it in the for loop)
            python3 client_runner.py
                Options:
                    --host (optional, default is 127.0.0.1)
                        server host name 
                    --port (optional, default is 1234)
                        server port
                    --stock_name (optional, default is GameStart)
                        stock name to lookup in the server
            
            Example: 
                python3 client_runner.py --host=elnux7.cs.umass.edu --port=1100 --stock_name=FishCo
        
        run.sh: (Shell script to run the above client_runner.py concurrently with configurable number of clients which can be changed inside the code. Currently the concurrent clients is configured to 5, we can change it inside the code in the for loop)
            bash run.sh
                Options:
                    1st argument: stockname (**REQUIRED**, gives error if not passed)
                    2nd argument: host (**REQUIRED**, gives error if not passed)
                    3rd argument: port (**REQUIRED**, gives error if not passed)
                **Note: The above order should be maintained strictly**

            Example:
                bash run.sh GameStart elnux1.cs.umass.edu 1234

## Part2:
    Server:
        python3 server.py
            Options:
                --num_threads (optional, default value is 2)
                    To initialize the threadpool with number of threads
                --gamestart_vol (optional, default value is 100)
                    maximum trading volume of the GameStart stock
                --fishco_vol (optional, default value is 100)
                    maximum trading volume of the FishCo stock
                --boarco_vol (optional, default value is 100)
                    maximum trading volume of the BoarCo stock
                --menhirco_vol (optional, default value is 100)
                    maximum trading volume of the MenhirCo stock

            Example:
                python3 server.py --num_threads=2 --gamestart_vol=300 --fishco_vol=200 --boarco_vol=250 --menhirco_vol=280
            
    Clients: In part2 we have different clients namely lookup, trade, price_updater, lookup_runner.py, trade_runner.py & run.sh
    
        Lookup client: (To lookup the given stock)
            python3 lookup.py
                Options:
                    --host (optional, default value is ‘127.0.0.1’)
                        to connect to server host
                    --stock_name (optional, default value is GameStart)
                        stock name to lookup
                    
                Example:
                    python3 lookup.py --host=elnux7.cs.umass.edu --stock_name=FishCo
        
        Trade client: (To trade the given stock with trading volume)
            python3 trade.py
                Options:
                    --host (optional, default value is ‘127.0.0.1’)
                        to connect to server host
                    --stock_name (optional, default value is GameStart)
                        stock name to trade
                    --trading_volume (optional, default value is 10)
                        trading volume to increment
                    --trading_type (optional, default value is BUY)
                        trading type (should be either BUY or SELL, and should be in uppercase)
                    
                Example:
                    python3 trade.py --host=elnux7.cs.umass.edu --stock_name=FishCo --trading_volume=20 --trading_type=SELL
                
        Price Updater client: (To update a random company's price with a random value)
            python3 price_updater.py
                Options:
                    --host (optional, default value is ‘127.0.0.1’)
                        to connect to server host
                    
                Example:
                    python3 price_updater.py --host=elnux7.cs.umass.edu
        
        Lookup Runner: Runs the lookup.py with sequential requests which is configurable inside the code(current value is 100). We can change the value inside the for loop.
            python3 lookup_runner.py
                Options:
                    --host (optional, default value is ‘127.0.0.1’)
                        to connect to server host
                    --stock_name (optional, default value is GameStart)
                        stock name to lookup
                    
                Example:
                    python3 lookup_runner.py --host=elnux7.cs.umass.edu --stock_name=FishCo
        
        Trade Runner: Runs the trade.py with sequential requests which is configurable inside the code(current value is 100). We can change the value inside the for loop.
            python3 trade_runner.py
                Options:
                    --host (optional, default value is ‘127.0.0.1’)
                        to connect to server host
                    --stock_name (optional, default value is GameStart)
                        stock name to trade
                    --trading_volume (optional, default value is 10)
                        trading volume to increment
                    --trading_type (optional, default value is BUY)
                        trading type (should be either BUY or SELL, and should be in uppercase)
                    
                Example:
                    python3 trade_runner.py --host=elnux7.cs.umass.edu --stock_name=FishCo --trading_volume=20 --trading_type=SELL

        run.sh: Shell script to run the above lookup_runner.py or trade_runner.py concurrenly with the configurable number of clients which can be changed inside the code (current value is 5). This value can be changed in the for loop.
            bash run.sh
                Options:
                    1st argument: stockname (**REQUIRED**, gives error if not passed)
                    2nd argument: host (**REQUIRED**, gives error if not passed)
                    3rd argument: program to run, can only be either lookup or trade (**REQUIRED**, gives error if not passed)
                
                Example:
                    To test the lookup method, pass lookup as the 3rd argument
                        bash run.sh GameStart elnux7.cs.umass.edu lookup
                    To test the trade method, pass trade as the 3rd argument
                        bash run.sh GameStart elnux7.cs.umass.edu trade
