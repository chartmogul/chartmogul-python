from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource


class Account(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#account
    """

    _path = "/account"

    class _Schema(Schema):
        name = fields.String()
        currency = fields.String()
        time_zone = fields.String()
        week_start_on = fields.String()

        @post_load
        def make(self, data, **kwargs):
            return Account(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def _validate_arguments(cls, method, kwargs):
        # no need for uuid validation on account
        return
