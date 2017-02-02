from marshmallow import Schema, fields, post_load
from ..resource import Resource, DataObject
from collections import namedtuple

"""
Beside the Customer class this module contains also subdocument classes.
These are used only on deserializing the server response, so the client has
proper types (eg. parsed dates instead of strings). Creating customer only
requires Customer class and simple dict/array data.
Validation is done on server.
"""

class Address(DataObject):
    class _Schema(Schema):
        address_zip = fields.String()
        city = fields.String()
        country = fields.String()
        state = fields.String()

        @post_load
        def make(self, data):
            return Address(**data)

class Stripe(DataObject):
    class _Schema(Schema):
        uid = fields.Int()
        coupon = fields.Boolean()

        @post_load
        def make(self, data):
            return Stripe(**data)

class Name(DataObject):
    class _Schema(Schema):
        fullName = fields.String()

        @post_load
        def make(self, data):
            return Name(**data)

class Employment(DataObject):
    class _Schema(Schema):
        name = fields.String()

        @post_load
        def make(self, data):
            return Employment(**data)

class Person(DataObject):
    class _Schema(Schema):
        name = fields.Nested(Name._Schema)
        employment = fields.Nested(Employment._Schema)

        @post_load
        def make(self, data):
            return Person(**data)

class Company(DataObject):
    class _Schema(Schema):
        name = fields.String()
        legalName = fields.String()
        domain = fields.String()
        url = fields.String()
        category = fields.Dict()
        metrics = fields.Dict()

        @post_load
        def make(self, data):
            return Company(**data)

class Clearbit(DataObject):
    class _Schema(Schema):
        company= fields.Nested(Company._Schema)
        person = fields.Nested(Person._Schema)

        @post_load
        def make(self, data):
            return Clearbit(**data)

class Attributes(DataObject):
    class _Schema(Schema):
        tags = fields.List(fields.String())
        stripe = fields.Nested(Stripe._Schema)
        clearbit = fields.Nested(Clearbit._Schema)
        custom = fields.Dict()

        @post_load
        def make(self, data):
            return Attributes(**data)

class Customer(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#plans
    """
    _path = "/customers{/uuid}"
    _root_key = 'entries'
    _many = namedtuple('Customers', [_root_key, "has_more", "per_page", "page", "current_page", "total_pages"])

    class _Schema(Schema):
        # All operations
        data_source_uuid = fields.String()
        external_id = fields.String()
        name = fields.String()
        company = fields.String()
        email = fields.String()
        city = fields.String()
        state = fields.String()
        country = fields.String()
        zip = fields.String()
        lead_created_at = fields.DateTime()
        free_trial_started_at = fields.DateTime()

        # Things that differ between create/update & retrieve/list
        attributes = fields.Nested(Attributes._Schema)

        # Retrieve/List only
        id = fields.Int()
        uuid = fields.String()
        external_ids = fields.List(fields.String())
        data_source_uuids = fields.List(fields.String())
        status = fields.String()
        customer_since = fields.DateTime(load_from="customer-since")
        mrr = fields.Number()
        arr = fields.Number()
        billing_system_url = fields.String(load_from="billing-system-url")
        chartmogul_url = fields.String(load_from="chartmogul-url")
        billing_system_type = fields.String(load_from="billing-system-type")
        currency = fields.String()
        currency_sign = fields.String(load_from="currency-sign")
        address = fields.Nested(Address._Schema)

        @post_load
        def make(self, data):
            return Customer(**data)

    _schema = _Schema(strict=True)
