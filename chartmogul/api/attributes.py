from marshmallow import Schema, fields, post_load
from ..resource import Resource, DataObject

class Attributes(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#customer-attributes
    """
    _path = "/customers{/uuid}/attributes"

    class _Schema(Schema):
        tags = fields.List(fields.String())
        stripe = fields.Dict()
        clearbit = fields.Dict()
        custom = fields.Dict()

        @post_load
        def make(self, data):
            return Attributes(**data)

    _schema = _Schema(strict=True)
