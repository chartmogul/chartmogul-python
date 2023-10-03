from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource, _add_method


class Ping(Resource):
    """
    https://dev.chartmogul.com/docs/authentication
    """

    _path = "/ping"

    class _Schema(Schema):
        data = fields.String()

        @post_load
        def make(self, data, **kwargs):
            return Ping(**data)

    _schema = _Schema(unknown=EXCLUDE)


_add_method(Ping, "ping", "get")
