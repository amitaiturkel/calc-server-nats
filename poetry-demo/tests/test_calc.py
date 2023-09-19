from nats.aio.client import Client as NATS
import json
import asyncio


nc = NATS()
async def start_nats_connection():
    await nc.connect("nats://localhost:4222")

async def close_nats_connection():
    await nc.close()

async def test_clear_client1_via_nats():

    subject = "calc"
    request_data = {
        "num": 3,
        "user_id": "test1",
        "operator": "clear"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 0

async def test_clear_client2_via_nats():

    subject = "calc"
    request_data = {
        "num": 3,
        "user_id": "test2",
        "operator": "clear"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 0

async def test_add_via_nats():

    subject = "calc"
    request_data = {
        "num": 3,
        "user_id": "test1",
        "operator": "add"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 3

async def test_subtract_via_nats():

    subject = "calc"
    request_data = {
        "num": 4,
        "user_id": "test1",
        "operator": "subtract"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == -1

async def test_multiply_via_nats():

    subject = "calc"
    request_data = {
        "num": 2,
        "user_id": "test1",
        "operator": "multiply"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == -2

async def test_divide_via_nats():

    subject = "calc"
    request_data = {
        "num": 10,
        "user_id": "test1",
        "operator": "divide"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == -0.2

async def test_divide_by_zero_via_nats():

    subject = "calc"
    request_data = {
        "num": 0,
        "user_id": "test1",
        "operator": "divide"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == -0.2


async def test_clear_via_nats():

    subject = "calc"
    request_data = {
        "user_id": "test1",
        "operator": "clear"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 0.0

async def test_put_in_via_nats():
    

    subject = "calc"
    request_data = {
        "num": 7,
        "user_id": "test1",
        "operator": "put_in"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 7

async def test_multiple_operations_via_nats():
    

    subject = "calc"
    
    # Add
    request_data = {
        "num": 5,
        "user_id": "test1",
        "operator": "add"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 12

    # Multiply
    request_data = {
        "num": 3,
        "user_id": "test1",
        "operator": "multiply"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 36

    # Subtract
    request_data = {
        "num": 2,
        "user_id": "test1",
        "operator": "subtract"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 34

async def test_invalid_operator_via_nats():
    

    subject = "calc"
    request_data = {
        "num": 5,
        "user_id": "test1",
        "operator": "invalid_operator"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 34
async def test_2_clients_via_nats():

    subject = "calc"
    request_data2 = {
        "num": 3,
        "user_id": "test2",
        "operator": "add"
    }
    response = await nc.request(subject, json.dumps(request_data2).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    assert result == 3
    request_data1 = {
        "num": 12,
        "user_id": "test1",
        "operator": "add"
    }
    #check if client 1 has change
    response = await nc.request(subject, json.dumps(request_data1).encode(), timeout=30)
    response_data1 = json.loads(response.data.decode())
    result = response_data1.get("result")
    assert result == 46


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_nats_connection())
    loop.run_until_complete(test_clear_client1_via_nats())
    loop.run_until_complete(test_add_via_nats())
    loop.run_until_complete(test_subtract_via_nats())
    loop.run_until_complete(test_multiply_via_nats())
    loop.run_until_complete(test_divide_via_nats())
    loop.run_until_complete(test_divide_by_zero_via_nats())
    loop.run_until_complete(test_clear_via_nats())
    loop.run_until_complete(test_put_in_via_nats())
    loop.run_until_complete(test_multiple_operations_via_nats())
    loop.run_until_complete(test_invalid_operator_via_nats())
    loop.run_until_complete(test_clear_client2_via_nats())
    loop.run_until_complete(test_2_clients_via_nats())
    loop.run_until_complete(close_nats_connection())
    loop.close()
