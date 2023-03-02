from datetime import date
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate
from service.models import Customer, Address

class CustomerFactory(factory.Factory):
    """Creates fake customers that you don't need to support :) """

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Customer

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")

class AddressFactory(factory.Factory):
    """ Creates fake addresses that you don't have to support """
    class Meta:
        """Maps factory to data model"""

        model = Address

    address_id = factory.Sequence(lambda n: n)
    street = FuzzyChoice(choices=["100 W 100 St.", "28-40 Jackson Ave"])
    city = factory.Faker("city")
    state = factory.Faker("state")
    country = factory.Faker("country")
    pin_code = FuzzyChoice(["11101", "68420"])
    customer_id = None
    # customer = factory.SubFactory(CustomerFactory)