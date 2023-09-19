import asyncio
import json
from nats.aio.client import Client as NATS

async def interact_with_calculator_via_nats():
    print("Welcome to the calculator program via NATS. Enter 'Q' to quit at any time.")
    user_id  = input("what is your user id? ")

    
    await nc.connect("nats://localhost:4222")
    while True:
        operator = input("Enter an operator ('add', 'subtract', 'multiply', 'divide', 'clear', 'put_in') or 'Q' to quit: ")
        

        if operator.lower() == "q":
            print("Exiting the program.")
            break
        
        elif operator not in ["add", "subtract", "multiply", "divide", "clear", "put_in"]:
            print("Invalid operator. Please enter a valid operator or 'Q' to quit.")
            continue
        if operator != "clear":
            try:
                num = float(input("Enter a number: "))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
        else:
            num = 0            
        subject = "calc"
        request_data = {
            "num": num,
            "user_id": user_id,
            "operator" :  operator
        }

        try:
            response = await nc.request(subject, json.dumps(request_data).encode(),timeout=30)
            response_data = json.loads(response.data.decode())
            result = response_data.get("result")
            print(f"Result: {result}")
        except Exception as e:
            print("An error occurred while communicating with the calculator service:", str(e))

if __name__ == "__main__":
        nc = NATS()
        asyncio.run(interact_with_calculator_via_nats())
