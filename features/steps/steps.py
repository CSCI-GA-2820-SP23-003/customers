######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Customer Steps
Steps file for customers.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given
from compare import expect


@given('the following customers')
def step_impl(context):
    """ Delete all Customers and Addresses, and load new ones """
    # List all of the customers and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/customers"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for customer in context.resp.json():
        for address in customer['addresses']:
            resp2 = requests.delete(f"{rest_endpoint}/{customer['id']}/addresses/{address['address_id']}")
            expect(resp2.status_code).to_equal(204)
        resp = requests.delete(f"{rest_endpoint}/{customer['id']}")
        expect(resp.status_code).to_equal(204)

    # load the database with new data
    for row in context.table:
        payload = {
            'first_name': row['firstname'],
            'last_name': row['lastname'],
            'email': row['email'],
            'password': row['password'],
            'active': row['active'] in ['True', 'true', '1'],
            'addresses': {}
        }

        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)

    context.resp = requests.get(rest_endpoint)
    customers = context.resp.json()
    # load the database with new data
    index = 0
    for row in context.table:
        payload = {
            "customer_id": customers[index]['id'],
            'street': row['street'],
            'city': row['city'],
            'state': row['state'],
            'country': row['country'],
            'pin_code': row['pincode']
        }
        index += 1
        context.resp = requests.post(f"{rest_endpoint}/{payload['customer_id']}/addresses", json=payload)
        expect(context.resp.status_code).to_equal(201)
