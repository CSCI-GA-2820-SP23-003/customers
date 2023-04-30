"""
The customers resource is a representation of the customer accounts.
All the REST API calls to the Customer or the Address Database are housed here.

Customers Service with Swagger and Flask RESTX
Paths:
------
GET / - Displays a UI for Selenium testing
GET /customers - Lists a list all of Customers
GET /customers/{customer_id} - Reads the Customer with given Customer ID
POST /customers - Creates a new Customer in the database
PUT /customers/{customer_id} - Updates a Customer with given customer ID
DELETE /customers/{customer_id} - Deletes a Customer with given ID
GET /customers/{customer_id}/addresses - Lists all the addresses of the customer with given ID
GET /customers/{customer_id}/addresses/{address_id} - Reads the Address with given ID of the customer with given ID
POST /customers/{customer_id}/addresses - Creates a new address of the customer with given Customer ID
PUT /customers/{customer_id}/addresses/{address_id} - Updates the address with given address ID of customer with given ID
DELETE /customers/{customer_id}/addresses/{address_id} - Deletes the address with given address ID of customer with given ID
PUT /customers/{customer_id}/activate - Activates a Customer with given Customer ID
PUT /customers/{customer_id}/deactivate - Deactivates a Customer with given Customer ID

"""
# pylint: disable=cyclic-import
from flask import jsonify
# from flask_restx import Api, Resource
from flask_restx import fields, reqparse, inputs, Resource
from service.common import status  # HTTP Status Codes
from service.models import Customer, Address

# Import Flask application
from . import app, api

create_address_model = api.model('Address', {
    'street': fields.String(required=True, description='The address street'),
    'city': fields.String(required=True, description='The address city'),
    'state': fields.String(required=True, description='The address state'),
    'country': fields.String(description='The address country'),
    'pin_code': fields.String(required=True, description='The address pin code'),
    'customer_id': fields.Integer(required=True, description='The customer ID corresponding to the Address')
})

address_model = api.inherit(
    'AddressModel',
    create_address_model,
    {
        'address_id': fields.Integer(readOnly=True, description='The unique id assigned internally by service')
    }
)

create_customer_model = api.model('Customer', {
    'first_name': fields.String(required=True, description='The First Name of the customer'),
    'last_name': fields.String(required=True, description='The Last Name of the customer'),
    'password': fields.String(required=True, description='The password of the customer'),
    'email': fields.String(required=True, description='The email of the customer'),
    'active': fields.Boolean(required=True, description='The active/inactive state of the customer'),
    'addresses': fields.List(fields.Nested(address_model,
                                           required=False,
                                           description='List of addresses that the customer has'))
})


customer_model = api.inherit(
    'CustomerModel',
    create_customer_model,
    {
        'id': fields.Integer(readOnly=True, description='The unique id assigned internally by service'),
    }
)

# query string arguments
customer_args = reqparse.RequestParser()
customer_args.add_argument('first_name', type=str, location='args', required=False, help='Find Customers by First Name')
customer_args.add_argument('last_name', type=str, location='args', required=False, help='Find Customers by Last Name')
customer_args.add_argument('email', type=str, location='args', required=False, help='Find Customers by Email')
customer_args.add_argument('active', type=inputs.boolean, location='args', required=False, help='Is the Customer active?')
customer_args.add_argument('street', type=str, location='args', required=False, help='Find Customers by Address street')
customer_args.add_argument('city', type=str, location='args', required=False, help='Find Customers by Address city')
customer_args.add_argument('state', type=str, location='args', required=False, help='Find Customers by Address state')
customer_args.add_argument('country', type=str, location='args', required=False, help='Find Customers by Address country')
customer_args.add_argument('pin_code', type=str, location='args', required=False, help='Find Customers by Address Pin Code')

############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return app.send_static_file('index.html')


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
#  PATH: /customers/{customer_id}
######################################################################
@api.route('/customers/<int:customer_id>')
@api.param('customer_id', 'The Customer identifier')
class CustomerResource(Resource):
    """
    CustomerResource class
    Allows the manipulation of a single customer
    GET /customer{customer_id} - Returns a Customer with the customer_id
    PUT /customer{customer_id} - Update a Customer with the customer_id
    DELETE /customer{customer_id} -  Deletes a Customer with the customer_id
    """

    # ------------------------------------------------------------------
    #  RETRIEVE A CUSTOMER
    # ------------------------------------------------------------------

    @api.doc('get_customers')
    @api.response(404, 'Customer not found')
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """
        Retrieve a single Customer
        This endpoint will return a Customer based on its ID.
        """
        app.logger.info("Request to Retrieve a Customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")
        app.logger.info('Returning customer: %s', customer.id)
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING CUSTOMER
    # ------------------------------------------------------------------

    @api.doc('update_customers')
    @api.response(404, 'Customer not found')
    @api.response(400, 'The posted Customer data was not valid')
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Update a Customer
        This endpoint will update a Customer based on the body that is posted.
        """
        app.logger.info('Request to Update a Customer with id [%s]', customer_id)
        customer = Customer.find(customer_id)
        original_password = None
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")
        else:
            original_password = customer.password
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        customer.deserialize(data)
        customer.id = customer_id
        customer.update(original_password)
        app.logger.info('Customer with ID [%s] updated.', customer.id)
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A CUSTOMER
    # ------------------------------------------------------------------

    @api.doc('delete_customers')
    @api.response(204, 'Customer deleted')
    def delete(self, customer_id):
        """
        Delete a Customer
        This endpoint will delete a Customer based on the ID specified in the path.
        """
        app.logger.info('Request to Delete a Customer with id [%s]', customer_id)
        customer = Customer.find(customer_id)
        if customer:
            customer.delete()
            app.logger.info('Customer with id [%s] was deleted', customer_id)
        return '', status.HTTP_204_NO_CONTENT

######################################################################
#  PATH: /customers
######################################################################


@api.route('/customers', strict_slashes=False)
class CustomerCollection(Resource):
    """ Handles all interactions with collections of Customers """
    # ------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    # ------------------------------------------------------------------

    @api.doc('list_customers')
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):
        """
        Lists all of the Customers
        This endpoint will list all the customers.
        """
        app.logger.info('Request to list customers...')
        customers = []
        args = customer_args.parse_args()
        if args['first_name']:
            app.logger.info('Filtering by first name: %s', args['first_name'])
            customers = Customer.find_by_first_name(args['first_name'])
        elif args['last_name']:
            app.logger.info('Filtering by last name: %s', args['last_name'])
            customers = Customer.find_by_last_name(args['last_name'])
        elif args['active'] is not None:
            app.logger.info('Filtering by active state: %s', args['active'])
            customers = Customer.find_by_active(args['active'])
        elif args['email']:
            app.logger.info('Filtering by email: %s', args['email'])
            customers = Customer.find_by_email(args['email'])
        elif args['street']:
            app.logger.info('Filtering by street: %s', args['street'])
            customers = Address.find_by_street(args['street'])
        elif args['city']:
            app.logger.info('Filtering by city: %s', args['city'])
            customers = Address.find_by_city(args['city'])
        elif args['state']:
            app.logger.info('Filtering by state: %s', args['state'])
            customers = Address.find_by_state(args['state'])
        elif args['country']:
            app.logger.info('Filtering by country: %s', args['country'])
            customers = Address.find_by_country(args['country'])
        elif args['pin_code']:
            app.logger.info('Filtering by pin code: %s', args['pin_code'])
            customers = Address.find_by_pin_code(args['pin_code'])
        else:
            app.logger.info('Returning unfiltered list.')
            customers = Customer.all()

        # app.logger.info('[%s] Customers returned', len(customers))
        results = [customer.serialize() for customer in customers]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    # ------------------------------------------------------------------

    @api.doc('create_customers')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_customer_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based on the data in the body that is posted.
        """
        app.logger.info('Request to Create a Customer')
        customer = Customer()
        app.logger.debug('Payload = %s', api.payload)
        customer.deserialize(api.payload)
        customer.create()
        app.logger.info('Customer with new id [%s] created!', customer.id)
        location_url = api.url_for(CustomerResource, customer_id=customer.id, _external=True)
        return customer.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

######################################################################
# Activate / Deactivate Customer
######################################################################

######################################################################
#  PATH: /customers/{customer_id}/activate
######################################################################


@api.route('/customers/<int:customer_id>/activate')
@api.param('customer_id', 'The Customer identifier')
class ActivateResource(Resource):
    """ Activate actions on a Customer """

    @api.doc('activate_customers')
    @api.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Activate a Customer
        This endpoint will activate a Customer.
        """
        app.logger.info(f'Request to Activate a Customer with ID: {customer_id}')
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f'Customer with id [{customer_id}] was not found.')
        customer.id = customer_id
        customer.active = True
        customer.update()
        app.logger.info('Customer with id [%s] has been activated!', customer.id)
        return customer.serialize(), status.HTTP_200_OK

######################################################################
#  PATH: /customers/{customer_id}/deactivate
######################################################################


@api.route('/customers/<int:customer_id>/deactivate')
@api.param('customer_id', 'The Customer identifier')
class DeactivateResource(Resource):
    """ Deactivate actions on a Customer """

    @api.doc('deactivate_customers')
    @api.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Deactivate a Customer
        This endpoint will deactivate a Customer.
        """
        app.logger.info(f'Request to Deactivate a Customer with ID: {customer_id}')
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f'Customer with id [{customer_id}] was not found.')
        customer.id = customer_id
        customer.active = False
        customer.update()
        app.logger.info('Customer with id [%s] has been deactivated!', customer.id)
        return customer.serialize(), status.HTTP_200_OK

######################################################################
#  PATH: /customers/{customer_id}/addresses/{address_id}
######################################################################


@api.route('/customers/<int:customer_id>/addresses/<int:address_id>')
@api.param('customer_id', 'The Customer identifier')
@api.param('address_id', 'The Address identifier')
class AddressResource(Resource):
    """
    AddressResource class
    Allows the manipulation of a single Address
    GET /customers/{customer_id}/addresses/{address_id} - Returns an Address with the id
    PUT /customers/{customer_id}/addresses/{address_id} - Update an Address with the id
    DELETE /customers/{customer_id}/addresses/{address_id} -  Deletes an Address with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ADDRESS
    # ------------------------------------------------------------------

    @api.doc('get_addresses')
    @api.marshal_with(address_model)
    @api.response(404, 'Address not found')
    def get(self, address_id, customer_id):
        """
        Retrieve an address
        This endpoint will return an address from a customer based on its ID.
        """
        app.logger.info('Request to retrieve an Address %s from Customer with id: %s', address_id, customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )
        address = Address.find(address_id)
        if not address or address.customer_id != customer.id:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Address with id '{address_id}' could not be found for the customer with id {customer.id}.",
            )
        app.logger.info('Returning address: %s', address.address_id)
        return address.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ADDRESS
    # ------------------------------------------------------------------

    @api.doc('update_addresses')
    @api.response(404, 'Address not found')
    @api.expect(address_model)
    @api.marshal_with(address_model)
    def put(self, address_id, customer_id):
        """
        Update an address of a customer
        This endpoint will update an Address based on the body that is posted.
        """

        app.logger.info('Request to Address with address_id [%s] and customer_id [%s] ...', address_id, customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

        # Find customer address with address_id
        addr_to_update = None
        for addr in customer.addresses:
            if addr.address_id == address_id:
                addr_to_update = addr
                break

        # if not found
        if not addr_to_update:
            abort(status.HTTP_404_NOT_FOUND, f"Address id '{address_id}' not found for customer '{customer_id}'.")
        data = api.payload
        addr_to_update.deserialize(data)
        addr_to_update.address_id = address_id
        addr_to_update.customer_id = customer_id
        addr_to_update.update()

        app.logger.info('Address with address_id [%s] and customer_id [%s] updated.', address_id, customer.id)
        return addr_to_update.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ADDRESS
    # ------------------------------------------------------------------

    @api.doc('delete_addresses')
    @api.response(204, 'Address deleted')
    def delete(self, address_id, customer_id):
        """
        Delete an address from a customer
        This endpoint will delete an Address based on the ID specified in the path.
        """
        app.logger.info('Request to delete address with address_id [%s] and customer_id [%s] ...', address_id, customer_id)

        address = Address.find(address_id)
        if address and address.customer_id == customer_id:
            address.delete()
            app.logger.info('Address with ID [%s] and customer ID [%s] delete completed.', address_id, customer_id)
        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /customers/{customer_id}/addresses
######################################################################
@api.route('/customers/<int:customer_id>/addresses', strict_slashes=False)
@api.param('customer_id', 'The Customer identifier')
class AddressCollection(Resource):
    """ Handles all interactions with collections of addresses """
    # ------------------------------------------------------------------
    # LIST ALL ADDRESSES FOR A CUSTOMER
    # ------------------------------------------------------------------

    @api.doc('list_addresses')
    @api.marshal_list_with(address_model)
    def get(self, customer_id):
        """
        List all of the addresses of a Customer
        This endpoint will list all addresses of a Customer.
        """
        app.logger.info('Request to list Addresses for Customer with id: %s', customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

        results = [address.serialize() for address in customer.addresses]
        app.logger.info("Returning %d addresses", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ADDRESS FOR A CUSTOMER
    # ------------------------------------------------------------------

    @api.doc('create_addresses')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_address_model)
    @api.marshal_with(address_model, code=201)
    def post(self, customer_id):
        """
        Create an address for a customer
        This endpoint will add a new address for a customer.
        """
        app.logger.info('Request to create an address for customer with id: %s', customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

        # Create an address instance for the customer = customer_id
        data = api.payload
        address = Address()
        address.deserialize(data)
        customer.addresses.append(address)
        customer.update()

        location_url = api.url_for(AddressResource,
                                   customer_id=address.customer_id,
                                   address_id=address.address_id,
                                   _external=True)
        app.logger.info('Address with ID [%s] created for Customer: [%s].', address.address_id, customer.id)
        return address.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)
