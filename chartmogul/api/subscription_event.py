from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class SubscriptionEvent(Resource):
    """
    https://dev.chartmogul.com/reference/subscription-events
    """

    _path = "/subscription_events"
    _root_key = "subscription_events"
    _many = namedtuple(
        "SubscriptionEvents", [_root_key, "has_more", "cursor"], defaults=[None, None]
    )

    class _Schema(Schema):
        id = fields.Int(required=True)
        data_source_uuid = fields.String(required=True)
        customer_external_id = fields.String(required=True)
        event_type = fields.String(required=True)
        event_date = fields.DateTime(required=True)
        effective_date = fields.DateTime(required=True)
        subscription_external_id = fields.String(allow_none=True)
        plan_external_id = fields.String(allow_none=True)
        currency = fields.String(allow_none=True)
        amount_in_cents = fields.Int(allow_none=True)
        quantity = fields.Int(allow_none=True)
        subscription_set_external_id = fields.String(allow_none=True)
        tax_amount_in_cents = fields.Int(allow_none=True)
        retracted_event_id = fields.String(allow_none=True)
        external_id = fields.String(allow_none=True)
        event_order = fields.Int(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return SubscriptionEvent(**data)

    _schema = _Schema(unknown=EXCLUDE)


SubscriptionEvent.all = SubscriptionEvent._method("all", "get", "/subscription_events")
SubscriptionEvent.destroy_with_params = SubscriptionEvent._method(
    "destroy_with_params", "delete", "/subscription_events"
)
SubscriptionEvent.modify_with_params = SubscriptionEvent._method(
    "modify_with_params", "patch", "/subscription_events"
)
