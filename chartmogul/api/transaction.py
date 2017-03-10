from marshmallow import Schema, fields, post_load
from ..resource import Resource
from collections import namedtuple


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

        @post_load
        def make(self, data):
            return Transaction(**data)

    _schema = _Schema(strict=True)
