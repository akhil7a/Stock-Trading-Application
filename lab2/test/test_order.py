import requests

# Function to test the order service to check if a trade request is success
def test_order_success():
    url = "http://localhost:8089/orders"
    # Input to the order service
    data = {
        "name":"GameStart",
        "quantity": 20,
        "type": "sell"
    }
    # Calling API using request module with json payload
    response = requests.post(url, json=data)
    # Checking if status code in response is success
    assert response.status_code == 200
    # Asserting if the transaction number is generated
    assert response.json()["transaction_number"] >= 0

# Function to test the order service to check trade request if incorrect stock is passed
def test_order_stock_not_found():
    url = "http://localhost:8089/orders"
    # Input to the order service with incorrect stock name
    data = {
        "name":"sample",
        "quantity": 20,
        "type": "sell"
    }
    # Calling API using request module with json payload
    response = requests.post(url, json=data)
    # Checking if status code in response is 404
    assert response.status_code == 404
    # Checking if the given stock is not found
    assert response.json()['error'] == 'Stock Not Found!'

# Function to test the order service to check if a trade request exceeded the quantity limit
def test_order_quantity_exceeded():
    url = "http://localhost:8089/orders"
    # Input to the order service with higher quantity
    data = {
        "name":"GameStart",
        "quantity": 200000,
        "type": "buy"
    }
    # Calling API using request module with json payload
    response = requests.post(url, json=data)
    # Checking if status code in response is 400
    assert response.status_code == 400
    # Checking if the given stock is exceeded the quantity limit
    assert response.json()['error'] == 'Quantity Exceeded Available Quantity!'
