from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource, _build_ext_id_params


class LineItem(Resource):
    """
    https://dev.chartmogul.com/reference/line-items
    Standalone resource for line item operations by external_id + data_source_uuid.
    """

    _path = "/line_items"
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

    @classmethod
    def retrieve(cls, config, **kwargs):
        """GET /line_items with data_source_uuid + external_id query params."""
        params = _build_ext_id_params(kwargs)
        return cls._request(config, "retrieve", "get", "/line_items", query_params=params)

    @classmethod
    def modify(cls, config, **kwargs):
        """PATCH /line_items with data_source_uuid + external_id query params."""
        params = _build_ext_id_params(kwargs)
        return cls._request(config, "modify", "patch", "/line_items",
                            data=kwargs.get("data"), query_params=params)

    @classmethod
    def destroy(cls, config, **kwargs):
        """DELETE /line_items with data_source_uuid + external_id query params."""
        params = _build_ext_id_params(kwargs)
        return cls._request(config, "destroy", "delete", "/line_items", query_params=params)

    @classmethod
    def toggle_disabled(cls, config, **kwargs):
        """PATCH /line_items/disabled_state with data_source_uuid + external_id query params."""
        params = _build_ext_id_params(kwargs)
        return cls._request(config, "modify", "patch", "/line_items/disabled_state",
                            data=kwargs.get("data"), query_params=params)
