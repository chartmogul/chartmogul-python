from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class Activity(Resource):
    """
    https://dev.chartmogul.com/reference/list-activities
    """

    _path = "/activities"
    _root_key = "entries"
    _many = namedtuple(
        "Activities", [_root_key, "has_more", "per_page", "cursor"], defaults=[None, None, None]
    )

    class _Schema(Schema):
        activity_arr = fields.Number(data_key="activity-arr")
        activity_mrr = fields.Number(data_key="activity-mrr")
        activity_mrr_movement = fields.Number(data_key="activity-mrr-movement")
        currency = fields.String()
        date = fields.DateTime()
        description = fields.String()
        type = fields.String()
        subscription_external_id = fields.String(data_key="subscription-external-id")
        plan_external_id = fields.String(data_key="plan-external-id")
        customer_name = fields.String(data_key="customer-name")
        customer_uuid = fields.String(data_key="customer-uuid")
        customer_external_id = fields.String(data_key="customer-external-id")
        billing_connector_uuid = fields.String(data_key="billing-connector-uuid")
        uuid = fields.String(data_key="uuid")

        @post_load
        def make(self, data, **kwargs):
            return Activity(**data)

    _schema = _Schema(unknown=EXCLUDE)
