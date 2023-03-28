"""
Models for Customer

All of the models are stored in this module
"""
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

# Function to initialize the database


def init_db(app):
    """ Initializes the SQLAlchemy app """
    Customer.init_db(app)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """


class Address(db.Model):
    """
    Class that represents a Address
    """

    ################
    # Address Schema
    ################

    # Table Schema
    address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'customer.id',
            ondelete="CASCADE"),
        nullable=False)

    def __repr__(self):
        return f"<Address {self.street} address_id=[{self.address_id}] customer[{self.customer_id}]>"

    def serialize(self):
        """
        Serializes an Address into a dictionary
        """
        return {"address_id": self.address_id,
                "street": self.street,
                "city": self.city,
                "state": self.state,
                "country": self.country,
                "pin_code": self.pin_code,
                "customer_id": self.customer_id
                }

    def deserialize(self, data):
        """
        Deserializes an Address from a dictionary

        Args:
            data (dict): A dictionary containing the Address data
        """
        try:
            self.street = data['street']
            self.city = data['city']
            self.state = data['state']
            self.country = data['country']
            self.pin_code = data['pin_code']
            self.customer_id = data['customer_id']
        except KeyError as error:
            raise DataValidationError(
                "Invalid Address: missing " +
                error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Address: Body of request contained bad or no data " +
                str(error)) from error
        return self

    def create(self):
        """
        Creates an Address in the database
        """
        logger.info('Creating %s', self.street)
        if not self.address_id:
            db.session.add(self)
        db.session.commit()
        logger.info("Address is saved successfully")

    def update(self):
        """
        Updates an Address in the database
        """
        logger.info("Updating/Saving %s, %s", self.street, self.city)
        if not self.address_id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Address from the database """
        logger.info("Deleting %s, %s", self.street, self.city)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_street(cls, street):
        """
       Returns customers whose addresses are in the street

        Args:
            street (string): the street of the Addresses you want to match
        """
        logger.info('Street query under progress for: %s ...', street)
        addresses = cls.query.filter(cls.street == street)
        return list(set([Customer.find(address.customer_id)
                    for address in addresses]))

    @classmethod
    def find_by_city(cls, city):
        """
        Returns customers whose addresses are in the given city

        Args:
            city (string): The addressess corresponding to the city you want to list
        """
        logger.info('City query under progress for: %s ...', city)
        addresses = cls.query.filter(cls.city == city)
        return list(set([Customer.find(address.customer_id)
                    for address in addresses]))

    @classmethod
    def find_by_state(cls, state):
        """
        Returns customers whose addresses are in the given state

        Args:
            state (string): The addresses corresponding to the state you want to list
        """
        logger.info('State query under progress for: %s ...', state)
        addresses = cls.query.filter(cls.state == state)
        return list(set(Customer.find(address.customer_id)
                    for address in addresses))

    @classmethod
    def find_by_pin_code(cls, pin_code):
        """
        Returns customers whose addresses have the given pin code

        Args:
            pin_code (string): the pin_code of the Addresses you want to match
        """
        logger.info('Pincode query under progress for: %s ...', pin_code)
        addresses = cls.query.filter(cls.pin_code == pin_code)
        return list(set(Customer.find(address.customer_id)
                    for address in addresses))

    @classmethod
    def find_by_country(cls, country):
        """
        Returns customers whose addresses are in the given country

        Args:
            country (string): the country of the Addresses you want to match
        """
        logger.info('Country query under progress for: %s ...', country)
        addresses = cls.query.filter(cls.country == country)
        return list(set(Customer.find(address.customer_id)
                    for address in addresses))

    @classmethod
    def find(cls, address_id):
        """ Finds a Address by it's ID """
        logger.info("Processing lookup for id %s ...", address_id)
        return cls.query.get(address_id)

    @classmethod
    def find_or_404_address(cls, address_id: int):
        """Find an Address by it's id

        :param address_id: the id of the Address to find
        :type address_id: int

        :return: an instance with the address_id, or 404_NOT_FOUND if not found
        :rtype: Address

        """
        logger.info("Processing lookup or 404 for id %s ...", address_id)
        logger.info("")
        return cls.query.get_or_404(address_id)


class Customer(db.Model):
    """
    Class that represents a Customer
    """

    ###############
    # Customer Schema
    ##############

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    addresses = db.relationship(
        "Address",
        backref="customer",
        passive_deletes=True)

    ###############
    # Instance Methods
    ##############

    def __repr__(self):
        return f"<Customer {self.last_name}, {self.first_name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s, %s", self.last_name, self.first_name)
        # id must be none to generate next primary key
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the database
        """
        logger.info("Updating/Saving %s, %s", self.last_name, self.first_name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s, %s", self.last_name, self.first_name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        customer = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "active": self.active,
            "addresses": [],
        }
        for address in self.addresses:
            customer["addresses"].append(address.serialize())
        return customer

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
            self.email = data["email"]
            self.password = data["password"]
            self.active = data["active"]
            # handle inner list of addresses
            address_list = data.get("addresses")
            for json_address in address_list:
                address = Address()
                address.deserialize(json_address)
                self.addresses.append(address)
        except KeyError as error:
            raise DataValidationError(
                "Invalid Customer: missing " +
                error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer: body of request contained bad or no data " +
                str(error)) from error
        return self

    ################
    # Class Methods
    ################

    @classmethod
    def init_db(cls, app: Flask):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Customer in the database """
        logger.info("Processing all Customer")
        return cls.query.all()

    @classmethod
    def find(cls, customer_id):
        """ Finds a Customer by it's ID """
        logger.info("Processing lookup for id %s ...", customer_id)
        return cls.query.get(customer_id)

    @classmethod
    def find_by_first_name(cls, first_name):
        """Returns all Customers with the given first_name

        :param name: the first_name of the Customers you want to match
        :type first_name: str

        :return: a collection of Customers with that first_name
        :rtype: list

        """
        logger.info("Processing first_name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)

    @classmethod
    def find_by_last_name(cls, last_name):
        """Returns all Customers with the given last_name

        :param name: the last_name of the Customers you want to match
        :type last_name: str

        :return: a collection of Customers with that last_name
        :rtype: list

        """
        logger.info("Processing last_name query for %s ...", last_name)
        return cls.query.filter(cls.last_name == last_name)

    @classmethod
    def find_by_email(cls, email):
        """Returns the Customer with the given email

        Args:
            email (string): the name of the Customer you want to match
        """
        logger.info("Processing name query for %s ...", email)
        return cls.query.filter(cls.email == email)

    @classmethod
    def find_or_404(cls, customer_id: int):
        """Find a Customer by it's id

        :param customer_id: the id of the Customer to find
        :type customer_id: int

        :return: an instance with the customer_id, or 404_NOT_FOUND if not found
        :rtype: Customer

        """
        logger.info("Processing lookup or 404 for id %s ...", customer_id)
        return cls.query.get_or_404(customer_id)
