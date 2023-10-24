from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class PlanGroupPlans(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#plan_groups
    """

    _path = "/plan_groups{/uuid}/plans"
    _root_key = "plans"
    _many = namedtuple("PlanGroupPlans", [_root_key, "has_more", "cursor"], defaults=[None, None])

    class _Schema(Schema):
        uuid = fields.String()
        data_source_uuid = fields.String()
        name = fields.String()
        interval_count = fields.Int()
        interval_unit = fields.String()
        external_id = fields.String()

        @post_load
        def make(self, data, **kwargs):
            return PlanGroupPlans(**data)

    _schema = _Schema(unknown=EXCLUDE)
