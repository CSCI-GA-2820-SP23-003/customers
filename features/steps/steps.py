"""
Steps for implementation of BDD Features/Scenarios
"""
from behave import given, then, when
from compare import expect
import logging
import requests

logger = logging.getLogger(__name__)

@given('the following customers')
def step_impl(context):
    """ Delete all Customers and Addresses, and load new ones """
    # List all of the customers and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/customers"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for customer in context.resp.json():
        resp = requests.delete(f"{rest_endpoint}/{customer['id']}")
        expect(resp.status_code).to_equal(204)
    
    # load the database with new data
    for row in context.table:
        addrData = row['addresses'].split(',')
        address = {}
        address['street'] = addrData[0]
        address['city'] = addrData[1]
        address['state'] = addrData[2]
        address['country'] = addrData[3]
        address['pin_code'] = addrData[4]
        address['customer_id'] = 0

        payload = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'active': row['active'] in ['True', 'true', '1'],
            'addresses': [address]
        }

        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
