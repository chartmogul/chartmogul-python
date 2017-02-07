from marshmallow import Schema, fields, post_load
from ..resource import Resource
from collections import namedtuple


class Activity(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#list-customer-subscriptions
    """
    _path = "/customers{/uuid}/activities"
    _root_key = 'entries'
    _many = namedtuple('Activities', [_root_key, "has_more", "per_page", "page"])

    class _Schema(Schema):
        id = fields.Int()
        activity_arr = fields.Number(load_from='activity-arr')
        activity_mrr = fields.Number(load_from='activity-mrr')
        activity_mrr_movement = fields.Number(load_from='activity-mrr-movement')
        currency = fields.String()
        currency_sign = fields.String(load_from='currency-sign')
        date = fields.DateTime()
        description = fields.String()
        type = fields.String()

        @post_load
        def make(self, data):
            return Activity(**data)

    _schema = _Schema(strict=True)
