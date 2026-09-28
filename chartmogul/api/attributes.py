from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource


class Attributes(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#customer-attributes
    """

    _path = "/customers{/uuid}/attributes"
    _bool_query_params = ["with_overrides"]

    class _Schema(Schema):
        tags = fields.List(fields.String())
        stripe = fields.Dict()
        clearbit = fields.Dict()
        custom = fields.Dict()
        overrides = fields.Dict()
        historical_values = fields.Dict()

        @post_load
        def make(self, data, **kwargs):
            return Attributes(**data)

    _schema = _Schema(unknown=EXCLUDE)
