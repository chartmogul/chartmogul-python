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
    _bool_query_params = ["completed"]

    class _Schema(Schema):

        task_uuid = fields.String()
        customer_uuid = fields.String(allow_none=True)
        # load_default=None keeps these attributes present even when the API omits them
        associated_object = fields.String(allow_none=True, load_default=None)
        associated_object_uuid = fields.String(allow_none=True, load_default=None)
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
