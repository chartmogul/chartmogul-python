from marshmallow import Schema, fields, post_load
from ..resource import Resource
from collections import namedtuple


class Subscription(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#list-customer-subscriptions
    """
    _path = "/customers{/uuid}/subscriptions"
    _root_key = 'entries'
    _many = namedtuple('Subscriptions', [_root_key, "has_more", "per_page", "page"])

    class _Schema(Schema):
        id = fields.Int()
        plan = fields.String()
        quantity = fields.Int()
        mrr = fields.Number()
        arr = fields.Number()
        status = fields.String()
        billing_cycle = fields.String(load_from='billing-cycle')
        billing_cycle_count = fields.Number(load_from='billing-cycle-count')
        start_date = fields.DateTime(load_from='start-date')
        end_date = fields.DateTime(load_from='end-date')
        currency = fields.String()
        currency_sign = fields.String(load_from='currency-sign')

        @post_load
        def make(self, data):
            return Subscription(**data)

    _schema = _Schema(strict=True)
