from marshmallow import Schema, fields, post_load
from ..resource import Resource, DataObject
from .transaction import Transaction
from collections import namedtuple


class LineItem(DataObject):

    class _Schema(Schema):
        uuid = fields.String()
        external_id = fields.String(allow_none=True)
        type = fields.String()
        subscription_uuid = fields.String()
        subscription_external_id = fields.String()
        plan_uuid = fields.String()
        prorated = fields.Boolean()
        service_period_start = fields.DateTime()
        service_period_end = fields.DateTime()
        amount_in_cents = fields.Int()
        quantity = fields.Int()
        discount_code = fields.String(allow_none=True)
        discount_amount_in_cents = fields.Int()
        tax_amount_in_cents = fields.Int()
        account_code = fields.String(allow_none=True)

        @post_load
        def make(self, data):
            return LineItem(**data)


class Invoice(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#invoices
    """
    _path = "/import/customers{/uuid}/invoices"
    _root_key = 'invoices'
    _many = namedtuple('Invoices', [_root_key, "current_page", "total_pages", "customer_uuid"])
    _many.__new__.__defaults__ = (None,) * len(_many._fields)

    class _Schema(Schema):
        uuid = fields.String()
        customer_uuid = fields.String(allow_none=True)
        external_id = fields.String(allow_none=True)
        date = fields.DateTime()
        due_date = fields.DateTime(allow_none=True)
        currency = fields.String()
        line_items = fields.Nested(LineItem._Schema, many=True)
        transactions = fields.Nested(Transaction._Schema, many=True)

        @post_load
        def make(self, data):
            return Invoice(**data)

    _schema = _Schema(strict=True)


Invoice.all_customer = Invoice.all
Invoice.all_any = Invoice._method('all', 'get', '/invoices')


def all(config, **kwargs):
    if 'uuid' in kwargs:
        return Invoice.all_customer(config, **kwargs)
    else:
        return Invoice.all_any(config, **kwargs)

Invoice.all = all
