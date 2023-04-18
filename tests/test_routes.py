"""
Customers API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import random

# pylint: disable=cyclic-import
# pylint: disable=too-many-lines
from unittest import TestCase
from service import app
from service.models import db, init_db, Address, Customer
from service.common import status  # HTTP Status Codes
from tests.factories import AddressFactory, CustomerFactory
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

app.logger.critical(DATABASE_URI)

BASE_URL = "/customers"
FLAG = False


######################################################################
#  M O D U L E   C O D E
######################################################################


# pylint: disable=invalid-name
def setUpModule():
    """ Sets up the database, and other attributes"""
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.logger.setLevel(logging.WARN)
    init_db(app)


def tearDownModule():
    """ Closes and drops the database"""
    db.session.close()
    db.drop_all()

######################################################################
#  T E S T   C A S E S
######################################################################


class TestCustomersServer(TestCase):
    # pylint: disable=too-many-public-methods
    """ Customers REST API Server Tests """

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

    ######################################################################
    #  A C T I V A T E / D E A C T I V A T E   C A S E S
    ######################################################################

    def test_activate_customer(self):
        """ It should activate customer """
        # Create dummy deactivated customers
        customers = CustomerFactory.create_batch(3)

        for customer in customers:
            customer.active = False
            customer.create()

        # choose a customer id randomly to delete
        all_customers = Customer.all()
        self.assertEqual(len(all_customers), 3)

        # pick random customer
        rand_customer = random.choice(all_customers)
        self.assertFalse(rand_customer.active)
        rand_customer_id = rand_customer.id

        # api call to activate the chosen customer
        resp = self.client.put(f"{BASE_URL}/{rand_customer_id}/activate")
        activated_customer = resp.get_json()

        self.assertEqual(rand_customer_id, activated_customer["id"])
        self.assertTrue(activated_customer["active"])
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_activate_invalid_customer(self):
        """ It should not activate invalid customer """

        resp = self.client.put(f"{BASE_URL}/10/activate")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivate_customer(self):
        """ It should deactivate customer """
        # Create dummy activated customers
        customers = CustomerFactory.create_batch(3)

        for customer in customers:
            customer.create()

        # choose a customer id randomly to delete
        all_customers = Customer.all()
        self.assertEqual(len(all_customers), 3)

        # pick random customer
        rand_customer = random.choice(all_customers)
        self.assertTrue(rand_customer.active)
        rand_customer_id = rand_customer.id

        # api call to activate the chosen customer
        resp = self.client.put(f"{BASE_URL}/{rand_customer_id}/deactivate")
        deactivated_customer = resp.get_json()

        self.assertEqual(rand_customer_id, deactivated_customer["id"])
        self.assertFalse(deactivated_customer["active"])
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_deactivate_invalid_customer(self):
        """ It should not deactivate invalid customer """

        resp = self.client.put(f"{BASE_URL}/10/deactivate")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ######################################################################
    #  R E A D   C A S E S
    ######################################################################

    def test_health(self):
        """It should get the health endpoint"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_index(self):
        """ Test case that checks if the home page is getting called"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_customer_list(self):
        """It should Get a list of Customers"""

        customers = CustomerFactory.create_batch(5)

        for customer in customers:
            customer.create()

        cust_get_req = self.client.get(BASE_URL)

        # Assert that the customer list is populated
        self.assertEqual(
            cust_get_req.status_code,
            status.HTTP_200_OK,
            "Customer list is populated successfully")
        data = cust_get_req.get_json()
        self.assertEqual(len(data), 5)

    def test_get_customer_by_first_name(self):
        """It should Get an Customer by First Name"""

        customers = CustomerFactory.create_batch(3)

        for customer in customers:
            customer.create()

        customers_list = [
            customer for customer in customers if customer.first_name == customers[0].first_name]
        resp = self.client.get(
            BASE_URL, query_string=f"first_name={customers[0].first_name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(customers_list))
        for record in data:
            self.assertEqual(record["first_name"], customers[0].first_name)

    def test_get_customer_by_last_name(self):
        """It should Get an Customer by Last Name"""

        customers = CustomerFactory.create_batch(3)

        for customer in customers:
            customer.create()

        customers_list = [
            customer for customer in customers if customer.last_name == customers[0].last_name]
        resp = self.client.get(
            BASE_URL, query_string=f"last_name={customers[0].last_name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(customers_list))
        for record in data:
            self.assertEqual(record["last_name"], customers[0].last_name)

    def test_get_customer_by_email(self):
        """It should Get an Customer by email"""

        customers = CustomerFactory.create_batch(3)

        for customer in customers:
            customer.create()

        customers_list = [
            customer for customer in customers if customer.email == customers[0].email]
        resp = self.client.get(
            BASE_URL, query_string=f"email={customers[0].email}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(customers_list))
        for record in data:
            self.assertEqual(record["email"], customers[0].email)

    def test_get_customer_by_active(self):
        """It should Get an Customer by active status"""

        customers = CustomerFactory.create_batch(3)

        customers[0].active = False
        customers[1].active = True
        customers[2].active = True
        for customer in customers:
            customer.create()

        active_found = self.client.get(
            BASE_URL, query_string="active=True")
        active_found = active_found.get_json()

        not_active_found = self.client.get(
            BASE_URL, query_string="active=False")
        not_active_found = not_active_found.get_json()

        self.assertEqual(len(active_found), 2)
        self.assertEqual(len(not_active_found), 1)

    def test_get_customer_by_street(self):
        """It should Get all the Customers by street"""

        customers = CustomerFactory.create_batch(2)
        addresses_to_add = AddressFactory.create_batch(4)

        # Create the addresses corresponding to the customers
        for idx, customer in enumerate(customers):
            customer.create()
            for addr_idx in range(2):
                addr = addresses_to_add[idx * 2 + addr_idx]
                resp = self.client.post(
                    f"{BASE_URL}/{customer.id}/addresses",
                    json=addr.serialize())
                self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        street_to_test = customers[0].addresses[0].street
        customers_list = []

        # Test if the number of returned customers is okay
        for customer in customers:
            for address in customer.addresses:
                if address.street == street_to_test:
                    customers_list.append(customer)
                    break

        resp = self.client.get(
            BASE_URL, query_string=f"street={street_to_test}")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()

        self.assertEqual(len(data), len(list(set(customers_list))))
        count = 0

        # Test if the returned customers have atleast one address satisfying
        # the constraints
        for record in data:
            # The loop breaks as soon as we find the eligible address since we
            # want to avoid counting duplicates
            for addr in record['addresses']:
                if addr['street'] == street_to_test:
                    count = count + 1
                    break

        self.assertEqual(len(customers_list), count)

    def test_get_customer_by_city(self):
        """It should Get all the Customers by city"""

        customers = CustomerFactory.create_batch(2)
        addresses_to_add = AddressFactory.create_batch(4)

        # Create the addresses corresponding to the customers
        for idx, customer in enumerate(customers):
            customer.create()
            for addr_idx in range(2):
                addr = addresses_to_add[idx * 2 + addr_idx]
                resp = self.client.post(
                    f"{BASE_URL}/{customer.id}/addresses",
                    json=addr.serialize())
                self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        city_to_test = customers[0].addresses[0].city
        customers_list = []

        # Test if the number of returned customers is okay
        for customer in customers:
            for address in customer.addresses:
                if address.city == city_to_test:
                    customers_list.append(customer)
                    break

        resp = self.client.get(
            BASE_URL, query_string=f"city={city_to_test}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()

        self.assertEqual(len(data), len(list(set(customers_list))))
        count = 0

        # Test if the returned customers have atleast one address satisfying
        # the constraints
        for record in data:
            # The loop breaks as soon as we find the eligible address since we
            # want to avoid counting duplicates
            for addr in record['addresses']:
                if addr['city'] == city_to_test:
                    count = count + 1
                    break

        self.assertEqual(len(customers_list), count)

    def test_get_customer_by_state(self):
        """It should Get all the Customers by state"""

        customers = CustomerFactory.create_batch(2)
        addresses_to_add = AddressFactory.create_batch(4)

        # Create the addresses corresponding to the customers
        for idx, customer in enumerate(customers):
            customer.create()
            for addr_idx in range(2):
                addr = addresses_to_add[idx * 2 + addr_idx]
                resp = self.client.post(
                    f"{BASE_URL}/{customer.id}/addresses",
                    json=addr.serialize())
                self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        state_to_test = customers[0].addresses[0].state
        customers_list = []

        # Test if the number of returned customers is okay
        for customer in customers:
            for address in customer.addresses:
                if address.state == state_to_test:
                    customers_list.append(customer)
                    break

        resp = self.client.get(
            BASE_URL, query_string=f"state={state_to_test}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()

        self.assertEqual(len(data), len(customers_list))
        count = 0

        # Test if the returned customers have atleast one address satisfying
        # the constraints
        for record in data:
            for addr in record['addresses']:
                if addr['state'] == state_to_test:
                    count = count + 1
                    break

        self.assertEqual(len(customers_list), count)

    def test_get_customer_by_pin_code(self):
        """It should Get all the Customers by pin code"""

        customers = CustomerFactory.create_batch(2)
        addresses_to_add = AddressFactory.create_batch(4)

        # Create the addresses corresponding to the customers
        for idx, customer in enumerate(customers):
            customer.create()
            for addr_idx in range(2):
                addr = addresses_to_add[idx * 2 + addr_idx]
                resp = self.client.post(
                    f"{BASE_URL}/{customer.id}/addresses",
                    json=addr.serialize())
                self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        pin_code_to_test = customers[0].addresses[0].pin_code
        customers_list = []

        # Test if the number of returned customers is okay
        for customer in customers:
            # The loop breaks as soon as we find the eligible address since we
            # want to avoid counting duplicates
            for address in customer.addresses:
                if address.pin_code == pin_code_to_test:
                    customers_list.append(customer)
                    break

        resp = self.client.get(
            BASE_URL, query_string=f"pin_code={pin_code_to_test}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()

        self.assertEqual(len(data), len(customers_list))
        count = 0

        # Test if the returned customers have atleast one address satisfying
        # the constraints
        for record in data:
            for addr in record['addresses']:
                if addr['pin_code'] == pin_code_to_test:
                    count = count + 1
                    break

        self.assertEqual(len(customers_list), count)

    def test_get_customer_by_country(self):
        """It should Get all the Customers by country"""

        customers = CustomerFactory.create_batch(2)
        addresses_to_add = AddressFactory.create_batch(4)

        # Create the addresses corresponding to the customers
        for idx, customer in enumerate(customers):
            customer.create()
            for addr_idx in range(2):
                addr = addresses_to_add[idx * 2 + addr_idx]
                resp = self.client.post(
                    f"{BASE_URL}/{customer.id}/addresses",
                    json=addr.serialize())
                self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        country_to_test = customers[0].addresses[0].country
        customers_list = []

        # Test if the number of returned customers is okay
        for customer in customers:
            for address in customer.addresses:
                if address.country == country_to_test:
                    customers_list.append(customer)
                    break

        resp = self.client.get(
            BASE_URL, query_string=f"country={country_to_test}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()

        self.assertEqual(len(data), len(customers_list))
        count = 0

        # Test if the returned customers have atleast one address satisfying
        # the constraints
        for record in data:
            # The loop breaks as soon as we find the eligible address since we
            # want to avoid counting duplicates
            for addr in record['addresses']:
                if addr['country'] == country_to_test:
                    count = count + 1
                    break

        self.assertEqual(len(customers_list), count)

    def test_get_customer(self):
        """It should Read a single Customer"""
        # get the id of an customer

        customer = CustomerFactory()
        # create the customer
        resp = self.client.post(BASE_URL, json=customer.serialize())
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            "Could not create test Customer"
        )
        new_customer = resp.get_json()
        customer.id = new_customer["id"]
        resp2 = self.client.get(
            f"{BASE_URL}/{customer.id}", content_type="application/json"
        )
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        data = resp2.get_json()
        self.assertEqual(data["id"], customer.id)
        self.assertEqual(data["first_name"], customer.first_name)
        self.assertEqual(data["last_name"], customer.last_name)
        self.assertEqual(data["email"], customer.email)
        self.assertEqual(data["password"], customer.password)

    def test_get_customer_not_found(self):
        """It should not Read a Customer that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        data = resp.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("Not Found", data["message"])

    ######################################################################
    #  C R E A T E  C A S E S
    ######################################################################

    def test_create_customer_valid_id(self):
        """It should check if a Customer has been created with a valid ID"""

        customers = CustomerFactory.create_batch(3)

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.client.post(BASE_URL, json=cust.serialize())

            # Assert that the customer has been created successfully
            self.assertEqual(
                cust_post_req.status_code,
                status.HTTP_201_CREATED,
                "Customer did not get created")

            created_customer = cust_post_req.get_json()
            self.assertIsNotNone(
                created_customer["id"],
                "IDs haven't been created")

    def test_create_customer_valid(self):
        """It should check if the Customer's fields have been populated correctly"""

        customers = CustomerFactory.create_batch(3)

        for cust in customers:
            logging.debug(cust)
            cust_post_req = self.client.post(BASE_URL, json=cust.serialize())

            # Assert that the customer has been created successfully
            self.assertEqual(
                cust_post_req.status_code,
                status.HTTP_201_CREATED,
                "Customer did not get created")

            created_customer = cust_post_req.get_json()
            self.assertEqual(
                created_customer["first_name"],
                cust.first_name,
                "First names are not matching")

            self.assertEqual(
                created_customer["last_name"],
                cust.last_name,
                "Last names are not matching")

            self.assertEqual(
                created_customer["email"],
                cust.email,
                "Emails are not matching")

            self.assertEqual(
                created_customer["password"],
                cust.password,
                "Passwords are not matching")

    ######################################################################
    #  D E L E T E   C A S E S
    ######################################################################

    def test_delete_customer_valid_request(self):
        """ It should delete a customer """
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()

        # choose a customer id randomly to delete
        all_customers = Customer.all()
        self.assertEqual(len(all_customers), 3)
        customer_id_to_delete = random.choice(all_customers).id

        # api call to delete the chosen customer
        resp = self.client.delete(f"{BASE_URL}/{customer_id_to_delete}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # checks to confirm the deletion
        deleted_customer = Customer.find(customer_id_to_delete)
        self.assertIsNone(deleted_customer)
        self.assertEqual(len(Customer.all()), 2)

    def test_delete_customer_invalid_request(self):
        """ It should not delete a customer but still return 204 """
        # deleting a customer that doesn't exist
        resp = self.client.delete(f"{BASE_URL}/1")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # deleting a customer multiple times
        customer = CustomerFactory()
        customer.create()
        _ = self.client.delete(f"{BASE_URL}/{customer.id}")  # first time
        resp = self.client.delete(f"{BASE_URL}/{customer.id}")  # second time
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    ##########################################
    # U P D A T E   C A S E S
    ##########################################

    def test_update_customer(self):
        """It should Update an existing Customer"""
        # create a Customer to update
        test_customer = CustomerFactory()
        response = self.client.post(BASE_URL, json=test_customer.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the Customer
        dummy_email = "User759@gmail.com"
        test_customer = response.get_json()
        logging.debug(test_customer)
        test_customer["email"] = dummy_email
        response = self.client.put(
            f"{BASE_URL}/{test_customer['id']}",
            json=test_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_customer = response.get_json()

        self.assertEqual(updated_customer["email"], dummy_email)
        self.assertEqual(updated_customer["id"], test_customer["id"])
        self.assertEqual(
            updated_customer["first_name"],
            test_customer["first_name"])
        self.assertEqual(
            updated_customer["last_name"],
            test_customer["last_name"])
        self.assertEqual(
            updated_customer["password"],
            test_customer["password"])

    def test_update_invalid_customer(self):
        """It should not Update Non existing Customer"""
        customer = CustomerFactory()
        customer.id = 10
        customer_ser = customer.serialize()
        logging.debug(customer)
        response = self.client.put(
            f"{BASE_URL}/{customer_ser['id']}",
            json=customer_ser)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer_invalid_content_type(self):
        """It should not Update an existing Customer with invalid content type request"""
        # create a Customer to update
        test_customer = CustomerFactory()
        response = self.client.post(BASE_URL, json=test_customer.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the Customer
        dummy_email = "User759@gmail.com"
        updated_customer = response.get_json()
        logging.debug(updated_customer)
        updated_customer["email"] = dummy_email
        response = self.client.put(
            f"{BASE_URL}/{updated_customer['id']}",
            json=updated_customer,
            content_type="custom_content_type_v100")
        self.assertEqual(
            response.status_code,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class TestAddressesServer(TestCase):
    # pylint: disable=too-many-public-methods
    """ Addresses REST API Server Tests """

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
    #  R E A D   C A S E S
    ######################################################################

    def test_list_address_invalid_cust_id(self):
        """ It should not list addresses of a Customer with invalid customer id"""

        customer = CustomerFactory()
        address = AddressFactory()
        customer.addresses.append(address)

        resp = self.client.get(f"{BASE_URL}/{customer.id}/addresses")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_address_list(self):
        """It should Get a list of Addresses"""
        # add two addresses to Customer

        customer = CustomerFactory.create_batch(1)[0]
        customer.create()

        address_list = AddressFactory.create_batch(2)

        # Create address 1
        resp = self.client.post(
            f"{BASE_URL}/{customer.id}/addresses",
            json=address_list[0].serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create address 2
        resp = self.client.post(
            f"{BASE_URL}/{customer.id}/addresses",
            json=address_list[1].serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2 addresses
        resp = self.client.get(f"{BASE_URL}/{customer.id}/addresses")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_get_address(self):
        """It should Read an address from a customer"""
        customer = CustomerFactory()
        # create the customer
        resp = self.client.post(BASE_URL, json=customer.serialize())
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            "Could not create test Customer"
        )
        new_customer = resp.get_json()
        customer.id = new_customer["id"]
        # create the address
        address = AddressFactory()
        address.customer_id = customer.id
        resp2 = self.client.post(
            f"{BASE_URL}/{customer.id}/addresses",
            json=address.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        new_address = resp2.get_json()
        address.address_id = new_address["address_id"]
        customer.addresses.append(address)
        resp3 = self.client.get(
            f"{BASE_URL}/{customer.id}/addresses/{address.address_id}",
            content_type="application/json",
        )
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        data = resp3.get_json()
        self.assertEqual(data["customer_id"], customer.id)
        self.assertEqual(data["customer_id"], address.customer_id)
        self.assertEqual(data["address_id"], address.address_id)
        self.assertEqual(data["street"], address.street)
        self.assertEqual(data["city"], address.city)
        self.assertEqual(data["state"], address.state)
        self.assertEqual(data["pin_code"], address.pin_code)
        self.assertEqual(data["country"], address.country)

    def test_get_address_not_found_valid_customer(self):
        """It should not Read an address that is not found for a valid customer ID"""
        # create the customer
        customer = CustomerFactory()
        resp = self.client.post(BASE_URL, json=customer.serialize())
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            "Could not create test Customer"
        )
        new_customer = resp.get_json()
        customer_id = new_customer["id"]
        resp2 = self.client.get(
            f"{BASE_URL}/{customer_id}/addresses/0",
            content_type="application/json",
        )
        self.assertEqual(resp2.status_code, status.HTTP_404_NOT_FOUND)
        data = resp2.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("Not Found", data["message"])

    def test_get_address_not_found_invalid_customer(self):
        """It should not Read an address for a customer that is not found"""
        response = self.client.get(f"{BASE_URL}/0/addresses/1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("Not Found", data["message"])

    ######################################################################
    #  C R E A T E   C A S E S
    ######################################################################

    def test_create_invalid_customer_valid_address_id(self):
        """It should check if the address fields are not populated for a random ID"""

        address = AddressFactory()
        cust_id = 0

        logging.debug(address)

        # make a post request to the address database
        addr_post_req = self.client.post(
            f"{BASE_URL}/{cust_id}/addresses",
            json=address.serialize())

        # assert that the address request had been created
        self.assertEqual(
            addr_post_req.status_code,
            status.HTTP_404_NOT_FOUND,
            "Address got created, should not have happened")

    def test_create_valid_customer_valid_address_id(self):
        """It should check if the Address' ID has been populated correctly"""

        customer = CustomerFactory()
        logging.debug(customer)

        # create the customer
        cust_post_req = self.client.post(BASE_URL, json=customer.serialize())

        # verify that the customer has been created
        self.assertEqual(
            cust_post_req.status_code,
            status.HTTP_201_CREATED,
            "Customer did not get created")
        created_customer = cust_post_req.get_json()

        # verify that the id has been created successfully
        self.assertIsNotNone(
            created_customer["id"],
            "IDs haven't been created")

        # retrieve the ID for the customer
        cust_id = created_customer["id"]

        # create the addresses now
        addresses = AddressFactory.create_batch(3)

        for addr in addresses:
            logging.debug(addr)

            # make a post request to the address database
            addr_post_req = self.client.post(
                f"{BASE_URL}/{cust_id}/addresses",
                json=addr.serialize())

            # assert that the address request had been created
            self.assertEqual(
                addr_post_req.status_code,
                status.HTTP_201_CREATED,
                "Address did not get created")
            created_addr = addr_post_req.get_json()
            self.assertIsNotNone(
                created_addr["address_id"],
                "Addresss ID has not been populated correctly")

    def test_create_valid_customer_valid_address(self):
        """It should check if the Address' fields have been populated correctly"""

        customer = CustomerFactory()
        logging.debug(customer)

        # create the customer
        cust_post_req = self.client.post(BASE_URL, json=customer.serialize())

        # verify that the customer has been created
        self.assertEqual(
            cust_post_req.status_code,
            status.HTTP_201_CREATED,
            "Customer did not get created")
        created_customer = cust_post_req.get_json()

        # verify that the id has been created successfully
        self.assertIsNotNone(
            created_customer["id"],
            "IDs haven't been created")

        # retrieve the ID for the customer
        cust_id = created_customer["id"]

        # create the addresses now
        addresses = AddressFactory.create_batch(3)

        for addr in addresses:
            logging.debug(addr)

            # make a post request to the address database
            addr_post_req = self.client.post(
                f"{BASE_URL}/{cust_id}/addresses",
                json=addr.serialize())

            # assert that the address request had been created
            self.assertEqual(
                addr_post_req.status_code,
                status.HTTP_201_CREATED,
                "Address did not get created")
            created_addr = addr_post_req.get_json()

            self.assertEqual(
                created_addr["street"],
                addr.street,
                "Addresss Streets has not been populated correctly")

            self.assertEqual(
                created_addr["city"],
                addr.city,
                "Addresss City has not been populated correctly")

            self.assertEqual(
                created_addr["state"],
                addr.state,
                "Addresss State has not been populated correctly")

            self.assertEqual(
                created_addr["country"],
                addr.country,
                "Addresss Country has not been populated correctly")

            self.assertEqual(
                created_addr["pin_code"],
                addr.pin_code,
                "Addresss pincode has not been populated correctly")

    ######################################################################
    #  D E L E T E   C A S E S
    ######################################################################

    def test_delete_address_valid_request(self):
        """ It should delete an address """
        customer = CustomerFactory()
        addresses = AddressFactory.create_batch(3)
        customer.addresses.extend(addresses)
        customer.create()
        self.assertEqual(len(customer.addresses), 3)

        # choose an address randomly to be deleted
        address_id_to_delete = random.choice(addresses).address_id

        # api call for deletion of address
        resp = self.client.delete(
            f"{BASE_URL}/{customer.id}/addresses/{address_id_to_delete}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # checks post-deletion of address
        deleted_address = Address.find(address_id_to_delete)
        self.assertIsNone(deleted_address)
        self.assertEqual(len(customer.addresses), 2)
        self.assertEqual(len(Address.query.all()), 2)

    def test_delete_address_invalid_request(self):
        """ It should not delete an address but still return 204 """
        # deleting an address that doesn't exist from a customer that doesn't
        # exist
        resp = self.client.delete(f"{BASE_URL}/1/addresses/1")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # deleting an address multiple times
        customer = CustomerFactory()
        address = AddressFactory()
        customer.addresses.append(address)
        customer.create()

        _ = self.client.delete(
            f"{BASE_URL}/{customer.id}/addresses/{address.address_id}")  # first time
        resp = self.client.delete(
            f"{BASE_URL}/{customer.id}/addresses/{address.address_id}")  # second time
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    ######################################################################
    #  U P D A T E   C A S E S
    ######################################################################

    def test_update_customer_address(self):
        """It should Update an existing Customer Address"""

        # create a Customer with 3 addresses to update
        customer = CustomerFactory()
        addresses = AddressFactory.create_batch(3)
        customer.addresses.extend(addresses)
        customer.create()
        customer_id = customer.id
        logging.debug(customer)
        # Check that customer been created
        customer = Customer.find(customer_id)
        self.assertIsNotNone(customer)
        # check that addresses been created
        self.assertEqual(len(customer.addresses), 3)

        # Pick an address randomly
        address_id_to_update = random.choice(customer.addresses).address_id
        # update the address
        address = Address.find(address_id_to_update)
        self.assertIsNotNone(address)
        dummy_street = "Washington Square"
        logging.debug(address)
        address = address.serialize()
        address["street"] = dummy_street

        response = self.client.put(
            f"{BASE_URL}/{address['customer_id']}/addresses/{address['address_id']}",
            json=address)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_address = Address.find(address['address_id'])
        logging.debug(updated_address)

        self.assertEqual(updated_address.address_id, address["address_id"])
        self.assertEqual(updated_address.customer_id, address["customer_id"])
        self.assertEqual(updated_address.country, address["country"])
        self.assertEqual(updated_address.state, address["state"])
        self.assertEqual(updated_address.city, address["city"])
        self.assertEqual(updated_address.pin_code, address["pin_code"])
        self.assertEqual(updated_address.street, dummy_street)

    def test_update_customer_address_invalid_customer(self):
        """It should not update address for an invalid Customer"""
        # create a Customer with an address to update
        customer = CustomerFactory()
        address = AddressFactory()
        customer.addresses.append(address)

        response = self.client.put(
            f"{BASE_URL}/{customer.id}/addresses/{address.address_id}",
            json=address.serialize())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer_address_invalid_address(self):
        """It should not update invalid address for a Customer"""
        # create a Customer with an address to update
        customer = CustomerFactory()
        customer.create()
        # check customer being created
        customer = Customer.find(customer.id)
        self.assertIsNotNone(customer)
        self.assertEqual(len(customer.addresses), 0)

        address = AddressFactory()
        response = self.client.put(
            f"{BASE_URL}/{customer.id}/addresses/{address.address_id}",
            json=address.serialize())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestBadRequests(TestCase):
    """ Tests for Bad Requests sent to Customers """

    def setUp(self):
        """ This runs before each test """
        db.session.query(Address).delete()
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def test_bad_request(self):
        """It should not Create when sending the wrong data"""
        resp = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create when sending wrong media type"""
        customer = CustomerFactory()
        resp = self.client.post(
            BASE_URL, json=customer.serialize(), content_type="test/html"
        )
        self.assertEqual(
            resp.status_code,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.put(BASE_URL, json={"not": "today"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_no_data(self):
        """It should not Create with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_content_type(self):
        """It should not Create with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
