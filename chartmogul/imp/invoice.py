from marshmallow import Schema, fields, post_load
from ..resource import Resource, DataObject
from .transaction import Transaction
from collections import namedtuple

class LineItem(DataObject):
    class _Schema(Schema):
        uuid = fields.String()
        external_id = fields.String()
        type = fields.String()
        subscription_uuid = fields.String()
        plan_uuid = fields.String()
        prorated = fields.Boolean()
        service_period_start = fields.DateTime()
        service_period_end = fields.DateTime()
        amount_in_cents = fields.Int()
        quantity = fields.Int()
        discount_code = fields.String()
        discount_amount_in_cents = fields.Int()
        tax_amount_in_cents = fields.Int()
        account_code = fields.String()

        @post_load
        def make(self, data):
            return LineItem(**data)

class Invoice(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#invoices
    """
    _path = "/import/customers{/uuid}/invoices"
    _root_key = 'invoices'
    _many = namedtuple('Invoices', [_root_key, "current_page", "total_pages"])

    class _Schema(Schema):
        uuid = fields.String()
        external_id = fields.String()
        date = fields.DateTime()
        due_date = fields.DateTime()
        currency = fields.String()
        line_items = fields.Nested(LineItem._Schema, many=True)
        transactions = fields.Nested(Transaction._Schema, many=True)

        @post_load
        def make(self, data):
            return Invoice(**data)

    _schema = _Schema(strict=True)
