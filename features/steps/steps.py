"""
Steps for implementation of BDD Features/Scenarios
"""
from behave import given
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
        addresses = []
        for adrs_data in row['addresses'].split(' '):
            if not adrs_data:
                continue
            adrs_data = adrs_data.split(',')
            address = {}
            address['street'] = adrs_data[0]
            address['city'] = adrs_data[1]
            address['state'] = adrs_data[2]
            address['country'] = adrs_data[3]
            address['pin_code'] = adrs_data[4]
            address['customer_id'] = 0
            addresses.append(address)

        payload = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'active': row['active'] in ['True', 'true', '1'],
            'addresses': addresses
        }

        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
