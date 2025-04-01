#! /bin/sh
stockname=$1

hostname=$2 # 2nd argument input from command line
method=$3
for j in {1..5}; do
    python3 $3_runner.py --stock_name=$stockname --host=$2 &
done
wait
