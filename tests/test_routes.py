"""
Customers API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
import random
from service import app
from service.models import db, init_db, Address, Customer
from service.common import status  # HTTP Status Codes
from tests.factories import AddressFactory, CustomerFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

app.logger.critical(DATABASE_URI)

BASE_URL = "/customers"

######################################################################
#  T E S T   C A S E S
######################################################################


class TestCustomersServer(TestCase):
    """ Customers REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.WARN)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Address).delete()
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()


    ######################################################################
    #  CUSTOMERS API TEST C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_customer_valid_request(self):
        """ It should delete a customer """
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        
        #choose a customer id randomly to delete
        all_customers = Customer.all()
        self.assertEqual(len(all_customers), 3)
        customer_id_to_delete = random.choice(all_customers).id
        
        #api call to delete the chosen customer
        resp = self.client.delete(f"{BASE_URL}/{customer_id_to_delete}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        #checks to confirm the deletion
        deleted_customer = Customer.find(customer_id_to_delete)
        self.assertIsNone(deleted_customer)
        self.assertEqual(len(Customer.all()), 2)

    def test_delete_customer_invalid_request(self):
        """ It should not delete a customer but still return 204 """
        #deleting a customer that doesn't exist
        resp = self.client.delete(f"{BASE_URL}/1")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        #deleting a customer multiple times
        customer = CustomerFactory()
        customer.create()
        _ = self.client.delete(f"{BASE_URL}/{customer.id}")    #first time
        resp = self.client.delete(f"{BASE_URL}/{customer.id}") #second time
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_address_valid_request(self):
        """ It should delete an address """
        customer = CustomerFactory()
        addresses = AddressFactory.create_batch(3)
        customer.addresses.extend(addresses)
        customer.create()
        self.assertEqual(len(customer.addresses), 3)

        #choose an address randomly to be deleted
        address_id_to_delete = random.choice(addresses).address_id

        #api call for deletion of address
        resp = self.client.delete(f"{BASE_URL}/{customer.id}/addresses/{address_id_to_delete}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        #checks post-deletion of address
        deleted_address = Address.find(address_id_to_delete)
        self.assertIsNone(deleted_address)
        self.assertEqual(len(customer.addresses), 2)
        self.assertEqual(len(Address.query.all()), 2)

    def test_delete_address_invalid_request(self):
        """ It should not delete an address but still return 204 """
        #deleting an address that doesn't exist from a customer that doesn't exist
        resp = self.client.delete(f"{BASE_URL}/1/addresses/1")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        #deleting an address multiple times
        customer = CustomerFactory()
        address = AddressFactory()
        customer.addresses.append(address)
        customer.create()

        _ = self.client.delete(f"{BASE_URL}/{customer.id}/addresses/{address.address_id}")    #first time
        resp = self.client.delete(f"{BASE_URL}/{customer.id}/addresses/{address.address_id}") #second time
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)