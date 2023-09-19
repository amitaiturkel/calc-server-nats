from nats.aio.client import Client as NATS
import json
import asyncio
import pytest
import pytest_asyncio

pytest_plugins = ('pytest_asyncio',)


nc = NATS()
async def get_responed(num,user_id,operator):
    subject = "calc"
    request_data = {
        "num": num,
        "user_id": f"{user_id}",
        "operator": f"{operator}"
    }
    response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
    response_data = json.loads(response.data.decode())
    result = response_data.get("result")
    return result

@pytest.mark.asyncio
async def test_start_nats_connection():
    await nc.connect("nats://localhost:4222")




@pytest.mark.asyncio
async def test_clear_client1_via_nats():
    assert await get_responed(3,"test1","clear" ) == 0
    

async def test_clear_client2_via_nats():
    assert await get_responed(3,"test2","clear" ) == 0


async def test_add_via_nats():
    assert await get_responed(3,"test1","add" ) == 3


async def test_subtract_via_nats():
    assert await get_responed(4,"test1","subtract" ) == -1


async def test_multiply_via_nats():
    assert await get_responed(3,"test1","multiply" ) == -3


async def test_divide_via_nats():
    assert await get_responed(10,"test1","divide" ) == -0.3


async def test_divide_by_zero_via_nats():
    assert await get_responed(0,"test1","divide" ) == -0.3



async def test_clear_via_nats():
    assert await get_responed(3,"test1","clear" ) == 0


async def test_put_in_via_nats():
    assert await get_responed(7,"test1","put_in" ) == 7


async def test_multiple_operations_via_nats():
    assert await get_responed(5,"test1","add" ) == 12
    assert await get_responed(3,"test1","multiply" ) == 36
    assert await get_responed(2,"test1","subtract" ) == 34


async def test_invalid_operator_via_nats():
    assert await get_responed(2,"test1","invalid_operator" ) == 34

async def test_2_clients_via_nats():
    assert await get_responed(3,"test2","add" ) == 3
    assert await get_responed(12,"test1","add" ) == 46


async def test_close_nats_connection():
    await nc.close()

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(test_start_nats_connection())
#     loop.run_until_complete(test_clear_client1_via_nats())
#     loop.run_until_complete(test_add_via_nats())
#     loop.run_until_complete(test_subtract_via_nats())
#     loop.run_until_complete(test_multiply_via_nats())
#     loop.run_until_complete(test_divide_via_nats())
#     loop.run_until_complete(test_divide_by_zero_via_nats())
#     loop.run_until_complete(test_clear_via_nats())
#     loop.run_until_complete(test_put_in_via_nats())
#     loop.run_until_complete(test_multiple_operations_via_nats())
#     loop.run_until_complete(test_invalid_operator_via_nats())
#     loop.run_until_complete(test_clear_client2_via_nats())
#     loop.run_until_complete(test_2_clients_via_nats())
#     loop.run_until_complete(test_close_nats_connection())
#     loop.close()
