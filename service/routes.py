"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Customer, Address

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...

######################################################################
# C R E A T E    A    N E W    C U S T O M E R
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """ Creates a customer instance in the database. The info is parsed
        from the request and the fields are populated using the appropriate
        methods in Customer class.
    """
    app.logger.info("Request to create a Customer")
    
    # Create the customer
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()

    # Create a message to return
    message = customer.serialize()
    #location_url = url_for("get_customers", customer_id=customer.id)

    # return make_response(
    #     jsonify(message), status.HTTP_201_CREATED, {"Location": location_url} 
    # )

    return make_response(
        jsonify(message), status.HTTP_201_CREATED
    )

######################################################################
# C R E A T E 
######################################################################
@app.route("/customers/<int:customer_id>/addresses", methods=["POST"])
def create_addresses(customer_id):
    """Creates an address linked to a specific customer"""

    app.logger.info(f"Request to create an address for a customer with {customer_id}")
    
    #get the customer information
    customer = Customer.find(customer_id)

    if not customer:
        abort(status.HTTP_404_NOT_FOUND, f"{customer_id} does not exist")

    #Create an address instance for the customer = customer_id
    address = Address()
    address.deserialize(request.get_json())

    customer.addresses.append(address)
    customer.update()

    #Create the final message that is to be sent
    to_send = address.serialize()

    return make_response(jsonify(to_send), status.HTTP_201_CREATED)






