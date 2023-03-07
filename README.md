# NYU DevOps Project - Customers Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

Customers Service - Representation of the Customers Accounts along with their Addresses at the eCommerce Website

## Overview

In this project, we have created a Customer Resource along with its subordinate - Address Resource as a part of an e-commerce website for the final project of the CSCI-GA-2820-SP23-003 - DevOps and Agile Methodologies course at NYU taught by Professor John Rofrano. Each customer will have address(es) corresponding to it.

## Running the service locally

To run the service, please use the command `flask run`. The service is available at localhost: `http://127.0.0.1:8000`

To run the all the test cases locally, please use the command `nosetests`. The test cases have 98% coverage currently.

## Contents

The `/service` folder contains the `models.py` file for the model and a `routes.py` file for the Customer service. The `/tests` folder has test cases code for testing the model and the service separately. 

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```
## Database Schema

We've used Postgres for our database that stores the Customer and Address Tables.

<img width="543" alt="image" src="https://user-images.githubusercontent.com/23705371/223218803-4b5ce9e9-3bdf-4bab-aa04-c1cb10638614.png">

## Customer Service APIs

### Index

GET `/`

### Customer Operations

| Description     | Endpoint                       
| --------------- | ------------------------------- 
| Create a Customer | POST `/customers` 
| Read/Get a Customer   | GET `/customers/{int:customer_id}`
| Update a Customer | PUT `/customers/{int:customer_id}` 
| Delete a Customer | DELETE `/customers/{int:customer_id}`
| List Customers     | GET `/customers`

### Address Operations

| Description     | Endpoint                        
| --------------- | -------------------------------
| Create an Address | POST `/customers/{int:customer_id}/addresses`
| Read/Get an Address   | GET `/customers/{int:customer_id}/addresses/{int:address_id}`
| Update an Address| PUT `/customers/{int:customer_id}/addresses/{int:address_id}`  
| Delete an Address| DELETE `/customers/{int:customer_id}/addresses/{int:address_id}`           
| List Addresses    | GET `/customers/{int:customer_id}/addresses`                  

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
