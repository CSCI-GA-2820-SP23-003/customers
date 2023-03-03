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
#  DELETE A CUSTOMER
######################################################################
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