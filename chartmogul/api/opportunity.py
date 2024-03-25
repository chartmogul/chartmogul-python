from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class Opportunity(Resource):
    """
    https://dev.chartmogul.com/reference/opportunities
    """

    _path = "/opportunities{/uuid}"
    _root_key = "entries"
    _many = namedtuple("Opportunities", [_root_key, "has_more", "cursor"])

    class _Schema(Schema):

        uuid = fields.String()
        customer_uuid = fields.String()
        owner = fields.String()
        pipeline = fields.String()
        pipeline_stage = fields.String()
        estimated_close_date = fields.Date()
        currency = fields.String()
        amount_in_cents = fields.Int()
        type = fields.String()
        forecast_category = fields.String()
        win_likelihood = fields.Int()
        custom = fields.Dict(allow_none=True)
        created_at = fields.DateTime()
        updated_at = fields.DateTime()

        @post_load
        def make(self, data, **kwargs):
            return Opportunity(**data)

    _schema = _Schema(unknown=EXCLUDE)
