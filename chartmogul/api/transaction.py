from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource


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

        @post_load
        def make(self, data, **kwargs):
            return Transaction(**data)

    _schema = _Schema(unknown=EXCLUDE)
