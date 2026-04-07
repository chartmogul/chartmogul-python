from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource, _build_ext_id_params


class Transaction(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#transactions
    """

    _path = "/import/invoices{/uuid}/transactions"

    class _Schema(Schema):
        uuid = fields.String()
        external_id = fields.String(allow_none=True)
        type = fields.String()
        date = fields.DateTime()
        result = fields.String()
        amount_in_cents = fields.Int(allow_none=True)
        transaction_fees_in_cents = fields.Int(allow_none=True)
        transaction_fees_currency = fields.String(allow_none=True)
        errors = fields.Dict(allow_none=True)
        disabled = fields.Boolean(allow_none=True)
        disabled_at = fields.DateTime(allow_none=True)
        disabled_by = fields.String(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return Transaction(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def retrieve_by_external_id(cls, config, **kwargs):
        """GET /transactions with data_source_uuid + external_id query params."""
        params = _build_ext_id_params(kwargs)
        return cls._request(config, "retrieve", "get", "/transactions", query_params=params)

    @classmethod
    def update_by_external_id(cls, config, **kwargs):
        """PATCH /transactions with data_source_uuid + external_id query params."""
        params = _build_ext_id_params(kwargs)
        return cls._request(config, "modify", "patch", "/transactions",
                            data=kwargs.get("data"), query_params=params)

    @classmethod
    def destroy_by_external_id(cls, config, **kwargs):
        """DELETE /transactions with data_source_uuid + external_id query params."""
        params = _build_ext_id_params(kwargs)
        return cls._request(config, "destroy", "delete", "/transactions", query_params=params)

    @classmethod
    def toggle_disabled_by_external_id(cls, config, **kwargs):
        """PATCH /transactions/disabled_state with data_source_uuid + external_id query params."""
        params = _build_ext_id_params(kwargs)
        return cls._request(config, "modify", "patch", "/transactions/disabled_state",
                            data=kwargs.get("data"), query_params=params)
