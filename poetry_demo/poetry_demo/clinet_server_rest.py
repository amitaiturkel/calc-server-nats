import httpx


async def interact_with_calculator1():
    print("Welcome to the calculator program. Enter 'Q' to quit at any time.")
    userid  = input("what is your user id? ")


    while True:
        operator = input("Enter an operator ('add', 'subtract', 'multiply', 'divide', 'clear', 'put_in') or 'Q' to quit: ")

        if operator.lower() == "q":
            print("Exiting the program.")
            break

        elif operator not in ["add", "subtract", "multiply", "divide", "clear", "put_in","nat"]:
            print("Invalid operator. Please enter a valid operator or 'Q' to quit.")
            continue
        num = 0
        if operator != "clear":
            try:
                num = float(input("Enter a number: "))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue

        url = f"http://localhost:8000/calculate/{operator}?num={num}"  # URL of the calculator service

        headers = {"user-id": f"{userid}"}  # desired user agent

        async with httpx.AsyncClient() as client:
            if operator == "put_in":
                response = await client.patch(url, headers=headers)
            elif operator == "clear":
                response = await client.delete(url)
            else:
                response = await client.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()["result"]
            print(f"Result: {result}")
        else:
            print("An error occurred while communicating with the calculator service.error code is ", response.status_code, url)


if __name__ == "__main__":
    import asyncio
    asyncio.run(interact_with_calculator1())
