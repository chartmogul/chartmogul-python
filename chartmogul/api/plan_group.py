from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from .plan_group_plans import PlanGroupPlans
from collections import namedtuple


class PlanGroup(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#plan_groups
    """

    _path = "/plan_groups{/uuid}"
    _root_key = "plan_groups"
    _many = namedtuple("PlanGroups", [_root_key, "has_more", "cursor"], defaults=[None, None])

    class _Schema(Schema):
        uuid = fields.String()
        name = fields.String()
        plans_count = fields.Int()

        @post_load
        def make(self, data, **kwargs):
            return PlanGroup(**data)

    _schema = _Schema(unknown=EXCLUDE)

    @classmethod
    def all(cls, config, **kwargs):
        """
        Actually uses two different endpoints, where it dispatches the call depends on whether
        uuid is given in the param or not.
        """
        if "uuid" in kwargs:
            return PlanGroupPlans.all(config, **kwargs)
        else:
            return cls.all_any(config, **kwargs)


PlanGroup.all_any = PlanGroup._method("all", "get", "/plan_groups")
