from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class Task(Resource):
    """
    https://dev.chartmogul.com/reference/tasks
    """

    _path = "/tasks{/uuid}"
    _root_key = "entries"
    _many = namedtuple("Tasks", [_root_key, "has_more", "cursor"])

    class _Schema(Schema):

        uuid = fields.String()
        customer_uuid = fields.String()
        assignee = fields.String()
        task_details = fields.String()
        due_date = fields.DateTime()
        completed_at = fields.DateTime(allow_none=True)
        created_at = fields.DateTime()
        updated_at = fields.DateTime()

        @post_load
        def make(self, data, **kwargs):
            return Task(**data)

    _schema = _Schema(unknown=EXCLUDE)
