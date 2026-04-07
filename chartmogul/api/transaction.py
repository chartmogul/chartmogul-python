from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource


class Transaction(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#transactions
    """

    _path = "/import/invoices{/uuid}/transactions"
    _ext_id_path = "/transactions"
    _bool_query_params = ['handle_as_user_edit']

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


Transaction.retrieve = Transaction._method(
    "retrieve", "get", "/transactions{/uuid}")
Transaction.modify = Transaction._method(
    "modify", "patch", "/transactions{/uuid}")
Transaction.destroy = Transaction._method(
    "destroy", "delete", "/transactions{/uuid}")
