#! /bin/sh
for j in {1..5}; do
    python3 client.py &
done
wait