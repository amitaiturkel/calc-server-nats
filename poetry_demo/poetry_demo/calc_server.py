from typing import Annotated, Dict
from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi
import asyncio
import json
from nats.aio.client import Client as NATS
import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
import uvicorn


class Calc:
    def __init__(self):
        self.result = 0.0

    def add(self, num):
        self.result += float(num)

    def subtract(self, num):
        self.result -= float(num)

    def multiply(self, num):
        self.result *= float(num)

    def divide(self, num):
        if float(num) != 0:
            self.result /= float(num)
        else:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")

    def put_in(self, num):
        self.result = float(num)

    def clear(self):
        self.result = 0.0

    def get_result(self):
        return self.result


app = FastAPI()




def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

users: Dict[str, str] = {}


def get_user_calc(user_id):
    if user_id not in users.keys():
        users[user_id] = Calc()
    return users[user_id]


def get_answer(calc, operator, num1=1):
    if operator == "add":
        calc.add(num1)
    elif operator == "subtract":
        calc.subtract(num1)
    elif operator == "multiply":
        calc.multiply(num1)
    elif operator == "divide":
        try:
            calc.divide(num1)
        except HTTPException:
            return calc.get_result()
    elif operator == "put_in":
        calc.put_in(num1)
    elif operator == "clear":
        calc.clear()
    else:
        raise HTTPException(status_code=400, detail="Invalid operator")
    return calc.get_result()

######################## rest server ############################
@app.get("/calculate/add")
async def add(num, user_id: Annotated[str | None, Header()] = None):
    calc = get_user_calc(user_id)
    operator = "add"
    result = get_answer(calc, operator, num)
    return {"result": result}


@app.get("/calculate/subtract")
async def subtract(num, user_id: Annotated[str | None, Header()] = None):
    calc = get_user_calc(user_id)
    operator = "subtract"
    result = get_answer(calc, operator, num)
    return {"result": result}


@app.get("/calculate/multiply")
async def multiply(num, user_id: Annotated[str | None, Header()] = None):
    calc = get_user_calc(user_id)
    operator = "multiply"
    result = get_answer(calc, operator, num)
    return {"result": result}


@app.get("/calculate/divide")
async def divide(num, user_id: Annotated[str | None, Header()] = None):
    calc = get_user_calc(user_id)
    operator = "divide"
    result = get_answer(calc, operator, num)
    return {"result": result}


@app.patch("/calculate/put_in")
async def put_in(num, user_id: Annotated[str | None, Header()] = None):
    calc = get_user_calc(user_id)
    operator = "put_in"
    result = get_answer(calc, operator, num)
    return {"result": result}


@app.delete("/calculate/clear")
async def clear(num=0, user_id: Annotated[str | None, Header()] = None):
    calc = get_user_calc(user_id)
    operator = "clear"
    result = get_answer(calc, operator)
    return {"result": result}


@app.get("/users")
async def read_item1():
    return {"result": users}


######################## nat server ############################



async def handle_message(msg):
    data = json.loads(msg.data.decode())
    operator = data.get("operator")
    
    num = data.get("num")
    user_id = data.get("user_id")
    calc = get_user_calc(user_id)
    try:
        result = get_answer(calc, operator, num)
    except HTTPException:
        result = get_answer(calc,'add',0)
    
    # Publish the result to the response subject
    response_subject = msg.reply
    try:
        await nc.publish(response_subject, json.dumps({"result": result}).encode())
    except Exception as e:
        # Handle the error 
        print(f"Error publishing message: {str(e)}")

async def start_server():
    await nc.connect("nats://localhost:4222")
    await nc.subscribe("calc", cb=handle_message)

######### running the NATS server ########
if __name__ == "__main__":
    nc = NATS()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server())
        print("the server is up and running")
        loop.run_forever()  # Keep the event loop running indefinitely

    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
    #### running the REST server: uvicorn.run(app, host="127.0.0.1", port=8000)
    



