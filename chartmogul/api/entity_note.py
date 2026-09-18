from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource
from collections import namedtuple


class EntityNote(Resource):
    """
    https://dev.chartmogul.com/reference/notes-and-call-logs/

    Notes and call logs attached to a customer or a contact (/v1/notes).
    Supersedes CustomerNote (/v1/customer_notes).
    """

    _path = "/notes{/uuid}"
    _root_key = "entries"
    _many = namedtuple("EntityNotes", [_root_key, "has_more", "cursor"], defaults=[None, None])

    class _Schema(Schema):
        uuid = fields.String()
        customer_uuid = fields.String(allow_none=True)
        # load_default=None keeps these attributes present even when the API omits them
        associated_object = fields.String(allow_none=True, load_default=None)
        associated_object_uuid = fields.String(allow_none=True, load_default=None)
        type = fields.String()
        text = fields.String()
        author = fields.String()
        call_duration = fields.Int()
        created_at = fields.DateTime()
        updated_at = fields.DateTime()

        @post_load
        def make(self, data, **kwargs):
            return EntityNote(**data)

    _schema = _Schema(unknown=EXCLUDE)
