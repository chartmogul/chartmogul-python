from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource


class LineItem(Resource):
    """
    https://dev.chartmogul.com/reference/line-items
    Standalone resource for line item operations by external_id + data_source_uuid.
    """

    _path = "/line_items"
    _ext_id_path = "/line_items"
    _bool_query_params = ['handle_as_user_edit']

    class _Schema(Schema):
        uuid = fields.String()
        external_id = fields.String(allow_none=True)
        type = fields.String()
        subscription_uuid = fields.String(allow_none=True)
        subscription_external_id = fields.String(allow_none=True)
        subscription_set_external_id = fields.String(allow_none=True)
        plan_uuid = fields.String(allow_none=True)
        prorated = fields.Boolean()
        service_period_start = fields.DateTime(allow_none=True)
        service_period_end = fields.DateTime(allow_none=True)
        amount_in_cents = fields.Int()
        quantity = fields.Int()
        discount_code = fields.String(allow_none=True)
        discount_amount_in_cents = fields.Int()
        discount_description = fields.String(allow_none=True)
        tax_amount_in_cents = fields.Int()
        transaction_fees_in_cents = fields.Int()
        transaction_fees_currency = fields.String(allow_none=True)
        account_code = fields.String(allow_none=True)
        description = fields.String(allow_none=True)
        event_order = fields.Int(allow_none=True)
        errors = fields.Dict(allow_none=True)
        disabled = fields.Boolean(allow_none=True)
        disabled_at = fields.DateTime(allow_none=True)
        disabled_by = fields.String(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return LineItem(**data)

    _schema = _Schema(unknown=EXCLUDE)


LineItem.create = LineItem._method(
    "create", "post", "/import/invoices{/uuid}/line_items")
LineItem.retrieve = LineItem._method("retrieve", "get", "/line_items{/uuid}")
LineItem.modify = LineItem._method("modify", "patch", "/line_items{/uuid}")
LineItem.destroy = LineItem._method("destroy", "delete", "/line_items{/uuid}")
LineItem.disable = LineItem._method(
    "disable", "patch", "/line_items{/uuid}/disabled_state")
