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


class Customer(db.Model):
    """
    Class that represents a Customer
    """

    ###############
    # Table Schema
    ##############

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Phone Number
    #phone_number = db.Column(db.String(255), nullable=True)
    
    ###############
    # Instance Methods
    ##############

    def __repr__(self):
        return f"<Customer {self.last_name}, {self.first_name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.name)
        # id must be none to generate next primary key
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the database
        """
        logger.info("Updating/Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "password": self.password
                }

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

        except KeyError as error:
            raise DataValidationError("Invalid Customer: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self

    ################
    ## Class Methods
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
