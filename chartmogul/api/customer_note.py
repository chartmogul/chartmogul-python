from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import Resource, _deprecated_method
from collections import namedtuple


class CustomerNote(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#customer-notes

    DEPRECATED: use EntityNote (/v1/notes) instead.
    """

    _path = "/customer_notes{/uuid}"
    _root_key = "entries"
    _many = namedtuple("CustomerNotes", [_root_key, "has_more", "cursor"])

    class _Schema(Schema):
        uuid = fields.String()
        customer_uuid = fields.String()
        type = fields.String()
        text = fields.String()
        author = fields.String()
        call_duration = fields.Int()
        created_at = fields.DateTime()
        updated_at = fields.DateTime()

        @post_load
        def make(self, data, **kwargs):
            return CustomerNote(**data)

    _schema = _Schema(unknown=EXCLUDE)


for _name, _verb in [
    ("all", "get"),
    ("create", "post"),
    ("retrieve", "get"),
    ("modify", "patch"),
    ("patch", "patch"),
    ("destroy", "delete"),
]:
    setattr(
        CustomerNote,
        _name,
        _deprecated_method(
            CustomerNote._method(_name, _verb),
            "CustomerNote.%s() is deprecated. Use EntityNote.%s() instead." % (_name, _name),
        ),
    )
