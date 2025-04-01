#! /bin/sh
stockname=$1
#hostname=$2 # 2nd argument input from command line
#port=$3   # 3rd argument input from command line
for j in {1..5}; do
    python3 client_runner.py --stock_name=$stockname --host=$2 --port=$3 &
    #python3 client_runner.py $stockname $hostname $port & #command to execute if all above 3 attributes are given through command line
done
wait