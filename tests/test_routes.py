"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import random

from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, Customer, Address, init_db
from service.common import status  # HTTP Status Codes


from tests.customer_factory import CustomerFactory, AddressFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/customers"
LOWER_LIMIT = 1
UPPER_LIMIT = 10

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerService(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.session.query(Customer).delete()
        db.session.commit()
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test case that checks if the home page is getting called"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_customer_valid_id(self):
        """Test case to check if the Customer ID is populated appropriately; happy paths"""

        customers = CustomerFactory.create_batch(random.randint(LOWER_LIMIT, UPPER_LIMIT))

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.app.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertIsNotNone(created_customer["id"], "IDs haven't been created")

    def test_create_customer_valid_first_name(self):
        """Test case to check if the Customer first name is populated appropriately; happy paths """

        customers = CustomerFactory.create_batch(random.randint(LOWER_LIMIT, UPPER_LIMIT))

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.app.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertEqual(created_customer["first_name"], cust.first_name, "First names are not matching")

    def test_create_customer_valid_last_name(self):
        """Test case to check if the Customer last name is populated appropriately; happy paths"""

        customers = CustomerFactory.create_batch(random.randint(LOWER_LIMIT, UPPER_LIMIT))

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.app.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertEqual(created_customer["last_name"], cust.last_name, "Last names are not matching")
    
    def test_create_customer_valid_email(self):
        """Test case to check if the Customer email is populated appropriately; happy paths"""

        customers = CustomerFactory.create_batch(random.randint(LOWER_LIMIT, UPPER_LIMIT))

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.app.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertEqual(created_customer["email"], cust.email, "Emails are not matching")

    def test_create_customer_valid_password(self):
        """Test case to check if the Customer password is populated appropriately; happy paths"""

        customers = CustomerFactory.create_batch(random.randint(LOWER_LIMIT, UPPER_LIMIT))

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.app.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertEqual(created_customer["password"], cust.password, "Passwords are not matching")

    def test_create_invalid_customer_valid_address_id(self):
        """Test case to check if the address fields are not populated for a random ID"""

        address = AddressFactory()
        cust_id = -100000

        logging.debug(address)

        #make a post request to the address database
        addr_post_req = self.app.post(f"{BASE_URL}/{cust_id}/addresses", json=address.serialize())

        print("Address post request", addr_post_req.status_code)

        #assert that the address request had been created
        self.assertEqual(addr_post_req.status_code, status.HTTP_404_NOT_FOUND, "Address got created, should not have happened")


    def test_create_valid_customer_valid_address_id(self):
        """Test case to check if the address fields are populated appropriately; happy paths"""

        customer = CustomerFactory()
        logging.debug(customer)

        #create the customer
        cust_post_req = self.app.post(BASE_URL, json=customer.serialize())

        #verify that the customer has been created
        self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")

        created_customer = cust_post_req.get_json()

        #verify that the id has been created successfully
        self.assertIsNotNone(created_customer["id"], "IDs haven't been created")

        #retrieve the ID for the customer
        cust_id = created_customer["id"]

        #create the addresses now

        addresses = AddressFactory.create_batch(random.randint(LOWER_LIMIT, UPPER_LIMIT))

        for addr in addresses:
            logging.debug(addr)

            #make a post request to the address database
            addr_post_req = self.app.post(f"{BASE_URL}/{cust_id}/addresses", json=addr.serialize())

            #assert that the address request had been created
            self.assertEqual(addr_post_req.status_code, status.HTTP_201_CREATED, "Address did not get created")

            created_addr = addr_post_req.get_json()
            self.assertIsNotNone(created_customer["id"], "Addresss ID has not been populated correctly")