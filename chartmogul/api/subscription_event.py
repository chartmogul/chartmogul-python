from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource, DataObject
from collections import namedtuple

class SubscriptionEvent(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#subscription_events
    """
    _path = "/subscription_events"
    _root_key = 'subscription_events'
    _many = namedtuple('SubscriptionEvents', [_root_key, 'meta'])
    #["next_key","prev_key","before_key","page","total_pages"]


    class _Schema(Schema):
        id = fields.Int()
        data_source_uuid = fields.String()
        customer_external_id = fields.String()
        event_type = fields.String()
        event_date = fields.Date()
        effective_date = fields.Date()
        subscription_external_id = fields.String()
        plan_external_id = fields.String()
        currency = fields.String()
        amount_in_cents = fields.Int()
        quantity = fields.Int()
        subscription_set_external_id = fields.String()
        tax_amount_in_cents = fields.Int()
        retracted_event_id = fields.String()
        external_id = fields.String(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return SubscriptionEvent(**data)

    _schema = _Schema(unknown=EXCLUDE)


SubscriptionEvent.all = SubscriptionEvent._method('all', 'get', '/subscription_events')
SubscriptionEvent.destroy_modify_with_params = SubscriptionEvent._method('destroy_with_params', 'delete', '/subscription_events')
SubscriptionEvent.modify_with_params = SubscriptionEvent._method('modify_with_params', 'patch', "/subscription_events")

#_add_method(Ping, "ping", "get")
