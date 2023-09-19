# Calculator Server and Interactive Clients

Welcome to the Calculator Server and Interactive Clients project! This repository contains a simple calculator server along with two interactive client scripts that interact with the server. Additionally, the project includes a folder with test cases for the calculator server.

## Getting Started

To get started with the project, follow these steps:

### Download the Project

Clone this repository to your local machine by running the following command in your terminal:

`git clone https://github.com/amitaiturkel/calc-server-nats`
go to calc-server-nats foldor 

### Set Up the Virtual Environment

Activate a virtual environment to isolate the project's dependencies. If you're using `virtualenv`, you can create and activate the environment with the following commands:

`python3 -m venv .venv` 
or run `python -m venv .venv`
and then
`source .venv/bin/activate`


### Install Dependencies

Use `poetry` to install the project's dependencies:

`poetry install`


This will ensure that all required packages are installed.

## Running the nats server
First use this tutorial to download the nats server :
'https://docs.nats.io/running-a-nats-service/introduction/installation'
then use this tutorial to run the nats server :
'https://devpress.csdn.net/linux/62e795eda254c06d462e2b51.html'

### Running the Calculator Server

To run the calculator server, execute the following command:
 
`python demo_poetry/calc_server.py` or `python3 demo_poetry/calc_server.py`
 
The server will start, and you'll be able to interact with it using the provided client scripts.
### Running Tests

After you made sure the Run the calculator server is running, test suite using the `tox` command:

`tox`


This will execute the test cases located in the `tests` folder to ensure the code's correctness.

### Using the Interactive Clients

Two interactive client scripts are provided as examples to interact with the server:

1. To use the first interactive client, navigate to the `demo_poetry` folder and run the following command:

`python client_server_nats.py` or  `python3 client_server_nats.py`


the client will allow you to perform various operations on the calculator server.


## Contributing

If you'd like to contribute to this project, please follow the standard GitHub pull request process.

## License

This project is licensed under the MIT License.
