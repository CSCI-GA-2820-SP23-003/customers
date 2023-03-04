"""
Customers API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import random

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
    #  C U S T O M E R S   A P I   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ Test case that checks if the home page is getting called"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_customer_valid_id(self):
        """Test case to check if the Customer ID is populated appropriately; happy paths"""

        customers = CustomerFactory.create_batch(3)

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.client.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertIsNotNone(created_customer["id"], "IDs haven't been created")

    def test_create_customer_valid_first_name(self):
        """Test case to check if the Customer first name is populated appropriately; happy paths """

        customers = CustomerFactory.create_batch(3)

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.app.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertEqual(created_customer["first_name"], cust.first_name, "First names are not matching")

    def test_create_customer_valid_last_name(self):
        """Test case to check if the Customer last name is populated appropriately; happy paths"""

        customers = CustomerFactory.create_batch(3)

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.client.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertEqual(created_customer["last_name"], cust.last_name, "Last names are not matching")
    
    def test_create_customer_valid_email(self):
        """Test case to check if the Customer email is populated appropriately; happy paths"""

        customers = CustomerFactory.create_batch(3)

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.client.post(BASE_URL, json=cust.serialize())

            #Assert that the customer has been created successfully
            self.assertEqual(cust_post_req.status_code, status.HTTP_201_CREATED, "Customer did not get created")
            
            created_customer = cust_post_req.get_json()
            self.assertEqual(created_customer["email"], cust.email, "Emails are not matching")

    def test_create_customer_valid_password(self):
        """Test case to check if the Customer password is populated appropriately; happy paths"""

        customers = CustomerFactory.create_batch(3)

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.client.post(BASE_URL, json=cust.serialize())

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
        addr_post_req = self.client.post(f"{BASE_URL}/{cust_id}/addresses", json=address.serialize())

        print("Address post request", addr_post_req.status_code)

        #assert that the address request had been created
        self.assertEqual(addr_post_req.status_code, status.HTTP_404_NOT_FOUND, "Address got created, should not have happened")


    def test_create_valid_customer_valid_address_id(self):
        """Test case to check if the address fields are populated appropriately; happy paths"""

        customer = CustomerFactory()
        logging.debug(customer)

        #create the customer
        cust_post_req = self.client.post(BASE_URL, json=customer.serialize())

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
            addr_post_req = self.client.post(f"{BASE_URL}/{cust_id}/addresses", json=addr.serialize())

            #assert that the address request had been created
            self.assertEqual(addr_post_req.status_code, status.HTTP_201_CREATED, "Address did not get created")

            created_addr = addr_post_req.get_json()
            self.assertIsNotNone(created_customer["id"], "Addresss ID has not been populated correctly")

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