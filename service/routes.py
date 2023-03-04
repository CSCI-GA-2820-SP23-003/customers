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
    location_url = url_for("get_customers", customer_id=customer.id)

    return make_response(
         jsonify(message), status.HTTP_201_CREATED, {"Location": location_url} 
     )

######################################################################
# C R E A T E    A    N E W    A D D R E S S
######################################################################
@app.route("/customers/<int:customer_id>/addresses", methods=["POST"])
def create_addresses(customer_id):
    """Creates an address linked to a specific customer"""

    app.logger.info(f"Request to create an address for a customer with {customer_id}")

    #get the customer information
    customer = Customer.find(customer_id)
    
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, f"Customer with {customer_id} does not exist")

    #Create an address instance for the customer = customer_id
    address = Address()
    address.deserialize(request.get_json())

    customer.addresses.append(address)
    customer.update()

    #Create the final message that is to be sent
    to_send = address.serialize()

    return make_response(jsonify(to_send), status.HTTP_201_CREATED)

######################################################################
# G E T    A    C U S T O M E R
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return an Customer based on its id
    """
    app.logger.info("Request for Customer with id: %s", customer_id)

    # See if the customer exists and abort if it doesn't
    customer = Customer.find(customer_id)
    if not customer:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' could not be found.",
        )

    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# G E T    A N    A D D R E S S     F R O M   C U S T O M E R
######################################################################
@app.route("/customers/<int:customer_id>/addresses/<int:address_id>", methods=["GET"])
def get_addresses(customer_id, address_id):
    """
    Get an Address
    This endpoint returns just an address
    """
    app.logger.info(
        "Request to retrieve Address %s for Customer id: %s", (address_id, customer_id)
    )

    # See if the address exists and abort if it doesn't
    address = Address.find(address_id)
    if not address:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{address_id}' could not be found.",
        )

    return make_response(jsonify(address.serialize()), status.HTTP_200_OK)

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """
    Deletes a Customer.
    Args:
    customer_id (int): unique id associated with the specific customer to be deleted.
    """
    app.logger.info("Request to delete customer: %s", customer_id)

    customer = Customer.find(customer_id)
    if customer:
        customer.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  DELETE AN ADDRESS
######################################################################
@app.route("/customers/<int:customer_id>/addresses/<int:address_id>", methods=["DELETE"])
def delete_address(customer_id, address_id):
    """
    Deletes an Address.

    Args:
        customer_id (int): customer id of the address we are trying to delete.
        address_id (int): id of the address we are trying to delete.
    """
    app.logger.info("Request to delete an address: %s of customer: %s", address_id, customer_id)

    address = Address.find(address_id)
    if address and address.customer_id == customer_id:
        address.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)