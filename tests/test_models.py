"""
Test cases for Customer Model

"""
import os
import logging
import unittest
from service.models import Customer, Address, DataValidationError, db
from service import app
from tests.customer_factory import CustomerFactory, AddressFactory
from werkzeug.exceptions import NotFound

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  Customer   M O D E L   T E S T   C A S E S
######################################################################
class TestCustomer(unittest.TestCase):
    """ Test Cases for Customer Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.query(Address).delete()
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_customer(self):
        """ It should Create a Customer and assert that it exists """
        customer = Customer(first_name="Marwan",last_name="J",email="mya6510@nyu.edu",password="12344321")
        self.assertEqual(str(customer), "<Customer J, Marwan id=[None]>")
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name,"Marwan")
        self.assertEqual(customer.last_name, "J")
        self.assertEqual(customer.email, "mya6510@nyu.edu")
        self.assertEqual(customer.password, "12344321")

    def test_add_customer(self):
        """It should Create a Customer and add it to the database"""
        customers = Customer.all()
        self.assertEqual(customers,[])
        customer = Customer(first_name="Marwan",last_name="J",email="mya6510@nyu.edu",password="12344321")
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, None)
        customer.create()
        self.assertIsNotNone(customer.id)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

    def test_read_customer(self):
        """It should Read a Customer and its Addresses"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        self.assertIsNotNone(customer.id)
        # Fetch it back
        found_customer = Customer.find(customer.id)
        self.assertEqual(found_customer.id, customer.id)
        self.assertEqual(found_customer.first_name, customer.first_name)
        self.assertEqual(found_customer.last_name, customer.last_name)
        self.assertEqual(found_customer.email, customer.email)
        self.assertEqual(found_customer.password, customer.password)
        self.assertEqual(found_customer.addresses, [])

    def test_update_a_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        logging.debug(customer)
        self.assertIsNotNone(customer.id)
        # Change it an save it
        customer.email = "mya6511@nyu.edu"
        original_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.email, "mya6511@nyu.edu")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, original_id)
        self.assertEqual(customers[0].email, "mya6511@nyu.edu")

    def test_update_no_id(self):
        """It should not Update a Customer with no id"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        self.assertRaises(DataValidationError, customer.update)

    def test_delete_a_customer(self):
        """It should Delete a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)

    def test_list_all_customers(self):
        """It should List all Customers in the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        # Create 5 Customers
        for _ in range(5):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 Customers
        customers = Customer.all()
        self.assertEqual(len(customers), 5)

    def test_serialize_a_customer(self):
        """It should serialize a Customer and its Addresses"""
        customer = CustomerFactory()
        address = AddressFactory()
        customer.addresses.append(address)
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], customer.id)
        self.assertIn("first_name", data)
        self.assertEqual(data["first_name"], customer.first_name)
        self.assertIn("last_name", data)
        self.assertEqual(data["last_name"], customer.last_name)
        self.assertIn("email", data)
        self.assertEqual(data["email"], customer.email)
        self.assertIn("password", data)
        self.assertEqual(data["password"], customer.password)
        self.assertEqual(len(data["addresses"]), 1)
        addresses = data["addresses"]
        self.assertEqual(addresses[0]["address_id"], address.address_id)
        self.assertEqual(addresses[0]["street"], address.street)
        self.assertEqual(addresses[0]["city"], address.city)
        self.assertEqual(addresses[0]["state"], address.state)
        self.assertEqual(addresses[0]["country"], address.country)
        self.assertEqual(addresses[0]["pin_code"], address.pin_code)
        self.assertEqual(addresses[0]["customer_id"], address.customer_id)

    def test_deserialize_a_customer(self):
        """It should Deserialize a Customer and its Addresses"""
        customer = CustomerFactory()
        customer.addresses.append(AddressFactory())
        customer.create()
        serial_customer = customer.serialize()
        new_customer = Customer()
        new_customer.deserialize(serial_customer)
        self.assertEqual(new_customer.id, None)
        self.assertEqual(new_customer.first_name, customer.first_name)
        self.assertEqual(new_customer.last_name, customer.last_name)
        self.assertEqual(new_customer.email, customer.email)
        self.assertEqual(new_customer.password, customer.password)

    def test_deserialize_missing_data(self):
        """It should not deserialize a Customer with missing data"""
        data = {"id": 1, "first_name": "Kitty", "email": "kitty@gmail.com"}
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_address_key_error(self):
        """It should not Deserialize an address with a KeyError"""
        address = Address()
        self.assertRaises(DataValidationError, address.deserialize, {})

    def test_deserialize_address_type_error(self):
        """It should not Deserialize an address with a TypeError"""
        address = Address()
        self.assertRaises(DataValidationError, address.deserialize, [])

    def test_add_customer_address(self):
        """It should Create an Customer with an Address and add it to the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = CustomerFactory()
        address = AddressFactory(customer=customer)
        customer.addresses.append(address)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(customer.id)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

        new_customer = customer.find(customer.id)
        self.assertEqual(new_customer.addresses[0].street, address.street)

        address2 = AddressFactory(customer=customer)
        customer.addresses.append(address2)
        customer.update()

        new_customer = Customer.find(customer.id)
        self.assertEqual(len(new_customer.addresses), 2)
        self.assertEqual(new_customer.addresses[1].street, address2.street)

    def test_update_account_address(self):
        """It should Update an Customer's address"""
        customers = Customer.all()
        self.assertEqual(customers, [])

        customer = CustomerFactory()
        address = AddressFactory(customer=customer)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(customer.id)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

        # Fetch it back
        customer = Customer.find(customer.id)
        old_address = customer.addresses[0]
        print("%r", old_address)
        self.assertEqual(old_address.city, address.city)
        # Change the city
        old_address.city = "XX"
        customer.update()

        # Fetch it back again
        customer = Customer.find(customer.id)
        address = customer.addresses[0]
        self.assertEqual(address.city, "XX")

    def test_delete_customer_address(self):
        """It should Delete a Customer's address"""
        customers = Customer.all()
        self.assertEqual(customers, [])

        customer = CustomerFactory()
        address = AddressFactory(customer=customer)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(customer.id)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

        # Fetch it back
        customer = Customer.find(customer.id)
        address = customer.addresses[0]
        address.delete()
        customer.update()

        # Fetch it back again
        customer = Customer.find(customer.id)
        self.assertEqual(len(customer.addresses), 0)

    def test_find_customer(self):
        """It should Find a Customer by ID"""
        customers = CustomerFactory.create_batch(5)
        for customer in customers:
            customer.create()
        logging.debug(customers)
        # make sure they got saved
        self.assertEqual(len(Customer.all()), 5)
        # find the 2nd customer in the list
        customer = Customer.find(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.first_name, customers[1].first_name)
        self.assertEqual(customer.last_name, customers[1].last_name)
        self.assertEqual(customer.email, customers[1].email)
        self.assertEqual(customer.password, customers[1].password)

    def test_find_by_first_name(self):
        """It should Find Customer by First Name"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        first_name = customers[0].first_name
        count = len([customer for customer in customers if customer.first_name == first_name])
        found = Customer.find_by_first_name(first_name)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.first_name, first_name)

    def test_find_by_last_name(self):
        """It should Find Customer by Last Name"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        last_name = customers[0].last_name
        count = len([customer for customer in customers if customer.last_name == last_name])
        found = Customer.find_by_last_name(last_name)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.last_name, last_name)

    def test_find_by_email(self):
        """It should Find Customer by Email"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        email = customers[0].email
        count = len([customer for customer in customers if customer.email == email])
        found = Customer.find_by_email(email)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.email, email)

    def test_find_or_404_found(self):
        """It should Find or return 404 not found"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()

        customer = Customer.find_or_404(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.first_name, customers[1].first_name)
        self.assertEqual(customer.last_name, customers[1].last_name)
        self.assertEqual(customer.email, customers[1].email)

    def test_find_or_404_not_found(self):
        """It should return 404 not found"""
        self.assertRaises(NotFound, Customer.find_or_404, 0)