"""
Beside the Customer class this module uses also subdocument classes.
These are used only on deserializing the server response, so the client has
proper types (eg. parsed dates instead of strings). Creating customer only
requires Customer class and simple dict/array data.
Validation is done on server.
"""
from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import DataObject, Resource
from collections import namedtuple
from .attributes import Attributes
from .contact import Contact
from .customer_note import CustomerNote
from .opportunity import Opportunity


class Address(DataObject):
    class _Schema(Schema):
        address_zip = fields.String(allow_none=True)
        city = fields.String(allow_none=True)
        country = fields.String(allow_none=True)
        state = fields.String(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return Address(**data)


class Customer(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#customers
    """

    _path = "/customers{/uuid}"
    _root_key = "entries"
    _many = namedtuple("Customers", [_root_key, "has_more", "cursor"], defaults=[None, None])

    class _Schema(Schema):
        # All operations
        data_source_uuid = fields.String()
        external_id = fields.String()
        name = fields.String()
        company = fields.String()
        email = fields.String()
        city = fields.String(allow_none=True)
        state = fields.String(allow_none=True)
        country = fields.String(allow_none=True)
        zip = fields.String(allow_none=True)
        lead_created_at = fields.DateTime(allow_none=True)
        free_trial_started_at = fields.DateTime(allow_none=True)

        # Things that differ between create/update & retrieve/list
        attributes = fields.Nested(Attributes._Schema, unknown=EXCLUDE)

        # Retrieve/List only
        id = fields.Int()
        uuid = fields.String()
        external_ids = fields.List(fields.String())
        data_source_uuids = fields.List(fields.String())
        status = fields.String()
        customer_since = fields.DateTime(data_key="customer-since", allow_none=True)
        mrr = fields.Number()
        arr = fields.Number()
        billing_system_url = fields.String(data_key="billing-system-url", allow_none=True)
        chartmogul_url = fields.String(data_key="chartmogul-url")
        billing_system_type = fields.String(data_key="billing-system-type")
        currency = fields.String()
        currency_sign = fields.String(data_key="currency-sign")
        address = fields.Nested(Address._Schema, allow_none=True, unknown=EXCLUDE)
        website_url = fields.String(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return Customer(**data)

    _schema = _Schema(unknown=EXCLUDE)


Customer.search = Customer._method("all", "get", "/customers/search")
Customer.merge = Customer._method("merge", "post", "/customers/merges")
Customer.connectSubscriptions = Customer._method(
    "create", "post", "/customers/{uuid}/connect_subscriptions"
)
Customer.contacts = Contact._method("all", "get", "/customers/{uuid}/contacts", useCallerClass=True)
Customer.createContact = Contact._method(
    "create", "post", "/customers/{uuid}/contacts", useCallerClass=True
)
Customer.notes = CustomerNote._method("all", "get", "/customer_notes?customer_uuid={uuid}", useCallerClass=True)
Customer.createNote = CustomerNote._method("create", "post", "/customer_notes", useCallerClass=True, useUUIDFor="customer_uuid")
Customer.opportunities = Opportunity._method("all", "get", "/opportunities?customer_uuid={uuid}", useCallerClass=True)
Customer.createOpportunity = Opportunity._method("create", "post", "/opportunities", useCallerClass=True, useUUIDFor="customer_uuid")
