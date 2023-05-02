# NYU DevOps Project - Customers Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-SP23-003/customers/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-003/customers/actions/workflows/tdd.yml)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP23-003/customers/branch/master/graph/badge.svg?token=1RWZZBE1PR)](https://codecov.io/gh/CSCI-GA-2820-SP23-003/customers)
[![Build Status](https://github.com/CSCI-GA-2820-SP23-003/customers/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-003/customers/actions/workflows/bdd.yml)

Customers Service - Representation of the Customers Accounts along with their Addresses at the eCommerce Website

## Overview

In this project, we have created a Customer Resource along with its subordinate - Address Resource as a part of an e-commerce website for the final project of the CSCI-GA-2820-SP23-003 - DevOps and Agile Methodologies course at NYU taught by Professor John Rofrano. Each customer will have address(es) corresponding to it.

## Running the service locally

To run the service, please use the command `honcho start`. The service is available at localhost: `http://127.0.0.1:8080`

To run all the test cases locally, please use the command `nosetests`. The test cases have 99% coverage currently.

To run the BDD tests, first start the service in a terminal by running `honcho start` and then run `behave` in another terminal.

## Using the service on Cloud/Kubernetes
The service is currently hosted on a Kubernetes Cluster on IBM Cloud.

Dev: http://159.122.179.165:31001/

Prod: http://159.122.179.165:31002/

## Flask-RESTX
The documentation for the api can be found here - `http://127.0.0.1:8080/apidocs` when running locally.    
Or on the cloud it can be found at `homeurl/apidocs`.

## Contents

The `/service` folder contains the `models.py` file for the model and a `routes.py` file for the Customer service. The `/tests` folder has test cases code for testing the model and the service separately. The `/features` folder contains the code for BDD testing of the service. And the `/deploy` folder contains the yaml files that can be used for deploying the file to a Kubernetes cluster.

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to fix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list of Python libraries required by your code
setup.cfg           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configs for the app
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands       - custom commands to use with flask
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants
└── static                 - code for UI of the homepage

tests/                - test cases package
├── __init__.py       - package initializer
├── factories.py      - factory to generate instances of model
├── test_cli_commands - tests custom flask cli commands
├── test_models.py    - test suite for business models
└── test_routes.py    - test suite for service routes

features/             - bdd test cases package
├── customers.feature - customers and address test scenarios
├── environment.py    - environment for bdd tests
└── steps             - code for describing bdd steps
    ├── steps.py      - steps for customers.feature
    ├── web_steps.py  - steps for web interaction with selenium

deploy/               - yaml files for kubernetes deployment
├── deployment.yaml   - Deployment for customers api
├── postgresql.yaml   - StatefulSet, Service, Secret for postgres db 
├── service.yaml      - Service for customers api

```
## Database Schema

We've used Postgres for our database that stores the Customer and Address Tables.

<img width="543" alt="image" src="https://user-images.githubusercontent.com/22293744/235336044-78df0398-fa6a-4b1f-92b2-febe15bc68d6.png">

## Customer Service APIs

### Index

GET `/`

### Base URL for all the APIs
`/api`

### Customer Operations

| Description     | Endpoint                       
| --------------- | ------------------------------- 
| Create a Customer | POST `/customers` 
| Read/Get a Customer   | GET `/customers/{int:customer_id}`
| Update a Customer | PUT `/customers/{int:customer_id}` 
| Delete a Customer | DELETE `/customers/{int:customer_id}`
| List Customers     | GET `/customers`
| Activate Customer  | PUT `/customers/{int:customer_id}/activate`
| Deactivate Customer  | PUT `/customers/{int:customer_id}/deactivate`


### Address Operations

| Description     | Endpoint                        
| --------------- | -------------------------------
| Create an Address | POST `/customers/{int:customer_id}/addresses`
| Read/Get an Address   | GET `/customers/{int:customer_id}/addresses/{int:address_id}`
| Update an Address| PUT `/customers/{int:customer_id}/addresses/{int:address_id}`  
| Delete an Address| DELETE `/customers/{int:customer_id}/addresses/{int:address_id}`           
| List Addresses    | GET `/customers/{int:customer_id}/addresses`  
| Search Customers and Addresses | GET `/customers/<query_field>=<query_value>`

## Customer Service APIs - Usage

### Create a Customer

URL : `http://127.0.0.1:8080/api/customers`

Method : POST

Auth required : No

Permissions required : None

Create a customer according to the provided first name, last name, email, password.

Example:

Request Body (JSON)
```json
{
  "first_name": "Akshama",
  "last_name": "AJ",
  "password": "aks",
  "email": "akshama@gmail.com",
  "active": true,
  "addresses": [
  ]
}
```

Success Response : `HTTP_201_CREATED`
```json
[
  {
    "id": 4,
    "first_name": "Akshama",
    "last_name": "AJ",
    "password": "b075b18d6e273c802744f832e3f4cb807b72922e92f203af671a45d3bbe3c658",
    "email": "akshama@gmail.com",
    "active": true,
    "addresses": []
  }
]
```

### Read/Get a Customer

URL : `http://127.0.0.1:8080/api/customers/{int:customer_id}`

Method : GET

Auth required : No

Permissions required : None

Gets/Reads a customer with id == customer_id provided in the URL

Example:

Success Response : `HTTP_200_OK`
```json
{
  "id": 4,
  "first_name": "Akshama",
  "last_name": "AJ",
  "password": "b075b18d6e273c802744f832e3f4cb807b72922e92f203af671a45d3bbe3c658",
  "email": "akshama@gmail.com",
  "active": true,
  "addresses": []
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```json
{
  "message": "Customer with id '5' was not found."
}
```

### Update a Customer

URL : `http://127.0.0.1:8080/api/customers/{int:customer_id}`

Method : PUT

Auth required : No

Permissions required : None

Updates a customer with id == customer_id provided in the URL according to the updated fields provided in the body

Example:

Request Body (JSON)
```json
{
  "first_name": "Akshama",
  "last_name": "Akshama",
  "password": "aks",
  "email": "akshama@gmail.com",
  "active": true,
  "addresses": [
  ],
  "id": 0
}
```

Success Response : `HTTP_200_OK`
```json
{
  "id": 4,
  "first_name": "Akshama",
  "last_name": "Akshama",
  "password": "b075b18d6e273c802744f832e3f4cb807b72922e92f203af671a45d3bbe3c658",
  "email": "akshama@gmail.com",
  "active": true,
  "addresses": []
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```json
{
  "message": "Customer with id '5' was not found."
}
```

### Delete a Customer

URL : `http://127.0.0.1:8080/api/customers/{int:customer_id}`

Method : DELETE

Auth required : No

Permissions required : None

Deletes a customer with id == customer_id

Example:

Success Response : `204 NO CONTENT`

### List Customers

URL : `http://127.0.0.1:8080/api/customers`

Method : GET

Auth required : No

Permissions required : None

Lists all the Customers

Example:

Success Response : `HTTP_200_OK`
```json
[
  {
    "id": 4,
    "first_name": "Akshama",
    "last_name": "Akshama",
    "password": "b075b18d6e273c802744f832e3f4cb807b72922e92f203af671a45d3bbe3c658",
    "email": "akshama@gmail.com",
    "active": true,
    "addresses": []
  }
]
```

### Activate Customers

URL : `http://127.0.0.1:8080/api/customers/{customer_id}/activate`

Method : PUT

Auth required : No

Permissions required : None

Activates a customer with id == customer_id

Example:

Success Response : `HTTP_200_OK`
```json
{
  "id": 4,
  "first_name": "Akshama",
  "last_name": "Akshama",
  "email": "akshama@gmail.com",
  "password": "b075b18d6e273c802744f832e3f4cb807b72922e92f203af671a45d3bbe3c658",
  "active": true,
  "addresses": []
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```json
{
  "message": "Customer with id [5] was not found."
}
```

### Deactivate Customers
URL : `http://127.0.0.1:8080/api/customers/{customer_id}/deactivate`

Method : PUT

Auth required : No

Permissions required : None

Deactivates a customer with id == customer_id

Example:

Success Response : `HTTP_200_OK`
```json
{
  "id": 4,
  "first_name": "Akshama",
  "last_name": "Akshama",
  "email": "akshama@gmail.com",
  "password": "b075b18d6e273c802744f832e3f4cb807b72922e92f203af671a45d3bbe3c658",
  "active": false,
  "addresses": []
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```json
{
  "message": "Customer with id [5] was not found."
}
```

### Create an Address
URL : `http://127.0.0.1:8080/api/customers/{int:customer_id}/addresses`

Method : POST

Auth required : No

Permissions required : None

Create an address according to the provided street, city, state, country, pin code and customer ID.

Example:

Request Body (JSON)
```json
{
  "street": "40 Pavonia Ave",
  "city": "Jersey City",
  "state": "NJ",
  "country": "USA",
  "pin_code": "07310",
  "customer_id": 4
}
```

Success Response : `HTTP_201_CREATED`
```json
{
  "address_id": 3,
  "street": "40 Pavonia Ave",
  "city": "Jersey City",
  "state": "NJ",
  "country": "USA",
  "pin_code": "07310",
  "customer_id": 4
}
```

Failure Response (When invalid Customer ID is provided in the URL) : `HTTP_404_NOT_FOUND`
```json
{
  "message": "Customer with id '5' was not found."
}
```

### Read/Get an Address

URL : `http://127.0.0.1:8080/api/customers/{int:customer_id}/addresses/{int:address_id}`

Method : GET

Auth required : No

Permissions required : None

Gets/Reads an address with id == address_id and customer id == customer_id provided in the URL

Example:

Success Response : `HTTP_200_OK`
```json
{
  "address_id": 3,
  "street": "40 Pavonia Ave",
  "city": "Jersey City",
  "state": "NJ",
  "country": "USA",
  "pin_code": "07310",
  "customer_id": 4
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```json
{
  "message": "Customer with id '5' was not found."
}
```

```json
{
  "message": "Address with id '4' could not be found for the customer with id 4."
}
```

### Update an Address

URL : `http://127.0.0.1:8080/api/customers/{int:customer_id}/addresses/{int:address_id}`

Method : PUT

Auth required : No

Permissions required : None

Updates an address with id == address_id and customer id == customer_id provided in the URL according to the updated fields provided in the body

Example:

Request Body (JSON)
```json
{
  "street": "40 Newport Pkwy",
  "city": "Jersey City",
  "state": "NJ",
  "country": "USA",
  "pin_code": "07310",
  "customer_id": 4,
  "address_id": 3
}
```

Success Response : `HTTP_200_OK`
```json
{
  "address_id": 3,
  "street": "40 Newport Pkwy",
  "city": "Jersey City",
  "state": "NJ",
  "country": "USA",
  "pin_code": "07310",
  "customer_id": 4
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```json
{
  "message": "Customer with id '5' was not found."
}
```

```json
{
  "message": "Address id '4' not found for customer '4'."
}
```

### Delete an Address

URL : `http://127.0.0.1:8080/api/customers/{int:customer_id}/addresses/{int:address_id}`

Method : DELETE

Auth required : No

Permissions required : None

Deletes an address with id == address_id and customer id == customer_id.

Example:

Success Response : `204 NO CONTENT`

### List Addresses

URL : `http://127.0.0.1:8080/api/customers/{int:customer_id}/addresses`

Method : GET

Auth required : No

Permissions required : None

Lists all the Addresses for a particular customer.

Example:

Success Response : `HTTP_200_OK`

```json
[
  {
    "address_id": 3,
    "street": "40 Newport Pkwy",
    "city": "Jersey City",
    "state": "NJ",
    "country": "USA",
    "pin_code": "07310",
    "customer_id": 4
  }
]
```

Failure Response : `HTTP_404_NOT_FOUND`
```json
{
  "message": "Customer with id '5' was not found."
}
```

### Search Customers and Addresses

URL : `http://127.0.0.1:8080/api/customers/<query_field>=<query_value>`

Method : GET

Auth required : No

Permissions required : None

Search for Customers and Addresses based on these query_fields - `first_name, last_name, email, active, street, city, state, country, pin_code`

Example:

Success Response for querying state=NJ : `HTTP_200_OK`

```json
[
  {
    "id": 4,
    "first_name": "Akshama",
    "last_name": "Akshama",
    "password": "b075b18d6e273c802744f832e3f4cb807b72922e92f203af671a45d3bbe3c658",
    "email": "akshama@gmail.com",
    "active": false,
    "addresses": [
      {
        "address_id": 3,
        "street": "40 Newport Pkwy",
        "city": "Jersey City",
        "state": "NJ",
        "country": "USA",
        "pin_code": "07310",
        "customer_id": 4
      }
    ]
  }
]
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
