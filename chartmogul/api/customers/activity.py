from marshmallow import Schema, fields, post_load, EXCLUDE
from chartmogul.resource import Resource
from collections import namedtuple


class CustomerActivity(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#list-customer-subscriptions
    """

    _path = "/customers{/uuid}/activities"
    _root_key = "entries"
    _many = namedtuple("Activities", [_root_key, "has_more", "cursor"], defaults=[None, None])

    class _Schema(Schema):
        id = fields.Int()
        activity_arr = fields.Number(data_key="activity-arr")
        activity_mrr = fields.Number(data_key="activity-mrr")
        activity_mrr_movement = fields.Number(data_key="activity-mrr-movement")
        currency = fields.String()
        currency_sign = fields.String(data_key="currency-sign")
        date = fields.DateTime()
        description = fields.String()
        type = fields.String()
        subscription_external_id = fields.String(data_key="subscription-external-id")

        @post_load
        def make(self, data, **kwargs):
            return CustomerActivity(**data)

    _schema = _Schema(unknown=EXCLUDE)
