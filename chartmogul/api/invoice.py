from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource, DataObject
from .transaction import Transaction
from collections import namedtuple


class LineItem(DataObject):
    class _Schema(Schema):
        uuid = fields.String()
        external_id = fields.String(allow_none=True)
        type = fields.String()
        subscription_uuid = fields.String(allow_none=True)
        subscription_external_id = fields.String(allow_none=True)
        subscription_set_external_id = fields.String(allow_none=True)
        plan_uuid = fields.String(allow_none=True)
        prorated = fields.Boolean()
        service_period_start = fields.DateTime(allow_none=True)
        service_period_end = fields.DateTime(allow_none=True)
        amount_in_cents = fields.Int()
        quantity = fields.Int()
        discount_code = fields.String(allow_none=True)
        discount_amount_in_cents = fields.Int()
        discount_description = fields.String(allow_none=True)
        tax_amount_in_cents = fields.Int()
        transaction_fees_in_cents = fields.Int()
        transaction_fees_currency = fields.String(allow_none=True)
        account_code = fields.String(allow_none=True)
        description = fields.String(allow_none=True)
        event_order = fields.Int(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return LineItem(**data)


class Invoice(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#invoices
    """

    _path = "/import/customers{/uuid}/invoices"
    _root_key = "invoices"
    _many = namedtuple(
        "Invoices",
        [_root_key, "cursor", "has_more", "customer_uuid"],
        defaults=[None, None, None],
    )
    _many.__new__.__defaults__ = (None,) * len(_many._fields)

    class _Schema(Schema):
        uuid = fields.String()
        external_id = fields.String(allow_none=True)
        customer_uuid = fields.String(allow_none=True)
        customer_external_id = fields.String(allow_none=True)
        data_source_uuid = fields.String(allow_none=True)

        currency = fields.String()
        date = fields.DateTime()
        due_date = fields.DateTime(allow_none=True)

        line_items = fields.Nested(LineItem._Schema, many=True, unknown=EXCLUDE)
        transactions = fields.Nested(Transaction._Schema, many=True, unknown=EXCLUDE)

        @post_load
        def make(self, data, **kwargs):
            return Invoice(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def all(cls, config, **kwargs):
        """
        Actually uses two different endpoints, where it dispatches the call depends on whether
        customer uuid is given with the old parameter name ('uuid') or not.
        """
        if "uuid" in kwargs:
            return super(Invoice, cls).all(config, **kwargs)
        else:
            return cls.all_any(config, **kwargs)


Invoice.all_any = Invoice._method("all", "get", "/invoices")
Invoice.destroy = Invoice._method("destroy", "delete", "/invoices{/uuid}")
Invoice.destroy_all = Invoice._method(
    "destroy_all",
    "delete",
    "/data_sources{/data_source_uuid}/customers{/customer_uuid}/invoices",
)
Invoice.retrieve = Invoice._method("retrieve", "get", "/invoices{/uuid}")
