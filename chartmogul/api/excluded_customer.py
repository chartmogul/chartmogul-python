from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class ReincludedCustomer(Resource):
    """
    Result of removing a customer from the exclude list with ExcludedCustomer.reinclude.
    """

    class _Schema(Schema):
        customer_uuid = fields.String()
        status = fields.String()

        @post_load
        def make(self, data, **kwargs):
            return ReincludedCustomer(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def _load(cls, response):
        # The API responds 202 with a body, which Resource._load would discard
        response.raise_for_status()
        return cls._loadJSON(response.json())


class ExcludedCustomer(Resource):
    """
    Customers on the account's exclude list, which keeps them from being
    re-imported. Each entry is one excluded data source customer, so the same
    customer_uuid can appear once per data source.
    """

    _path = "/excluded_customers{/uuid}"
    _root_key = "entries"
    _many = namedtuple("ExcludedCustomers", [_root_key, "has_more", "cursor"], defaults=[None, None])

    class _Schema(Schema):
        customer_uuid = fields.String()
        data_source_uuid = fields.String(allow_none=True)
        external_id = fields.String(allow_none=True)
        name = fields.String(allow_none=True)
        email = fields.String(allow_none=True)
        excluded_at = fields.DateTime(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return ExcludedCustomer(**data)

    _schema = _Schema(unknown=EXCLUDE)


ExcludedCustomer.reinclude = ReincludedCustomer._method(
    "destroy", "delete", "/excluded_customers{/uuid}", useCallerClass=True
)
