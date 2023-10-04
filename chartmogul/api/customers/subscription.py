from marshmallow import Schema, fields, post_load, EXCLUDE
from chartmogul.resource import Resource
from collections import namedtuple


class CustomerSubscription(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#list-customer-subscriptions
    https://dev.chartmogul.com/v1.0/reference#list-a-customers-subscriptions
    """

    _path = "/customers{/uuid}/subscriptions"
    _root_key = "entries"
    _many = namedtuple("Subscriptions", [_root_key, "has_more", "cursor"], defaults=[None, None])

    class _Schema(Schema):
        id = fields.Int(allow_none=True)
        plan = fields.String(allow_none=True)
        quantity = fields.Int(allow_none=True)
        mrr = fields.Number(allow_none=True)
        arr = fields.Number(allow_none=True)
        status = fields.String(allow_none=True)
        billing_cycle = fields.String(data_key="billing-cycle", allow_none=True)
        billing_cycle_count = fields.Number(data_key="billing-cycle-count", allow_none=True)
        start_date = fields.DateTime(data_key="start-date", allow_none=True)
        end_date = fields.DateTime(data_key="end-date", allow_none=True)
        currency = fields.String(allow_none=True)
        currency_sign = fields.String(data_key="currency-sign", allow_none=True)

        # /import namespace
        uuid = fields.String(allow_none=True)
        external_id = fields.String(allow_none=True)
        subscription_set_external_id = fields.String(allow_none=True)
        plan_uuid = fields.String(allow_none=True)
        customer_uuid = fields.String(allow_none=True)
        data_source_uuid = fields.String(allow_none=True)
        cancellation_dates = fields.List(fields.DateTime(), allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return CustomerSubscription(**data)

    _schema = _Schema(unknown=EXCLUDE)

    # /import has different paging
    @classmethod
    def _loadJSON(cls, jsonObj):
        if "subscriptions" in jsonObj:
            _many = namedtuple(
                "Subscriptions",
                ["subscriptions", "has_more", "cursor", "customer_uuid"],
            )
            return _many(
                cls._schema.load(jsonObj["subscriptions"], many=True),
                customer_uuid=jsonObj.get("customer_uuid", None),
                has_more=jsonObj.get("has_more", None),
                cursor=jsonObj.get("cursor", None),
            )
        else:
            return super(CustomerSubscription, cls)._loadJSON(jsonObj)


# /import namespace
CustomerSubscription.list_imported = CustomerSubscription._method(
    "list_imported", "get", "/import/customers{/uuid}/subscriptions"
)
CustomerSubscription.cancel = CustomerSubscription._method(
    "cancel", "patch", "/import/subscriptions{/uuid}"
)
CustomerSubscription.modify = CustomerSubscription._method(
    "modify", "patch", "/import/subscriptions{/uuid}"
)
