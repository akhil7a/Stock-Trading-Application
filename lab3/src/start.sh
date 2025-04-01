#!/bin/bash

cd backend/catalog

nohup python3 app.py --port 3000 > catalog_3000.log &

cd ../order

nohup python3 app.py --port 4000 > order_4000.log &
nohup python3 app.py --port 4001 > order_4001.log &
nohup python3 app.py --port 4002 > order_4002.log &

cd ../../frontend

nohup python3 app.py > frontend.log &