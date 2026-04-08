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
        disabled = fields.Bool(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return SubscriptionEvent(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def _wrap_envelope(cls, kwargs):
        """Wrap params in subscription_event envelope.

        Supports three call styles (all backwards compatible):
        1. New style:     (config, id=123, data={'amount': 2000})
        2. Flat style:    (config, data={'id': 123, 'amount': 2000})
        3. Envelope style:(config, data={'subscription_event': {'id': 123}})
        """
        data = dict(kwargs.get("data", {}))
        if "subscription_event" in data:
            return data
        # Merge top-level id/external_id/data_source_uuid into data
        for key in ("id", "external_id", "data_source_uuid"):
            if key in kwargs:
                data[key] = kwargs[key]
        return {"subscription_event": data}

    @classmethod
    def destroy_with_params(cls, config, **kwargs):
        """DELETE /subscription_events. Accepts flat or envelope-wrapped params."""
        kwargs["data"] = cls._wrap_envelope(kwargs)
        return cls._destroy_raw(config, **kwargs)

    @classmethod
    def modify_with_params(cls, config, **kwargs):
        """PATCH /subscription_events. Accepts flat or envelope-wrapped params."""
        kwargs["data"] = cls._wrap_envelope(kwargs)
        return cls._modify_raw(config, **kwargs)

    @classmethod
    def disable(cls, config, **kwargs):
        """Disable a subscription event by setting disabled to true."""
        data = dict(kwargs.get("data", {}))
        if "subscription_event" in data:
            data = dict(data["subscription_event"])
        for key in ("id", "external_id", "data_source_uuid"):
            if key in kwargs:
                data[key] = kwargs[key]
        data["disabled"] = True
        return cls.modify_with_params(config, data=data)

    @classmethod
    def enable(cls, config, **kwargs):
        """Enable a subscription event by setting disabled to false."""
        data = dict(kwargs.get("data", {}))
        if "subscription_event" in data:
            data = dict(data["subscription_event"])
        for key in ("id", "external_id", "data_source_uuid"):
            if key in kwargs:
                data[key] = kwargs[key]
        data["disabled"] = False
        return cls.modify_with_params(config, data=data)


SubscriptionEvent.all = SubscriptionEvent._method(
    "all", "get", "/subscription_events")
SubscriptionEvent._destroy_raw = SubscriptionEvent._method(
    "destroy_with_params", "delete", "/subscription_events")
SubscriptionEvent._modify_raw = SubscriptionEvent._method(
    "modify_with_params", "patch", "/subscription_events")
