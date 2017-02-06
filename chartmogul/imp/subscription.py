from marshmallow import Schema, fields, post_load
from ..resource import Resource
from collections import namedtuple


class Subscription(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#subscriptions
    """
    _path = "/import/customers{/uuid}/subscriptions"
    _root_key = 'subscriptions'
    _many = namedtuple('Subscriptions', [_root_key, "current_page", "total_pages", "customer_uuid"])


    class _Schema(Schema):
        uuid = fields.String()
        external_id = fields.String()
        plan_uuid = fields.String()
        customer_uuid = fields.String()
        data_source_uuid = fields.String()
        cancellation_dates = fields.List(fields.DateTime())

        @post_load
        def make(self, data):
            return Subscription(**data)

    _schema = _Schema(strict=True)

Subscription.cancel = Subscription._method('cancel', 'patch', "/import/subscriptions{/uuid}")
Subscription.modify = Subscription._method('modify', 'patch', "/import/subscriptions{/uuid}")
