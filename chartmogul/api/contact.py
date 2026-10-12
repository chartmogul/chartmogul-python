from marshmallow import Schema, fields, post_load, EXCLUDE
from ..resource import ASSOCIATED_OBJECT_CONTACT, Resource
from collections import namedtuple
from .entity_note import EntityNote
from .task import Task


class Contact(Resource):
    """
    https://dev.chartmogul.com/v1.0/reference#contacts
    """

    _path = "/contacts{/uuid}"
    _root_key = "entries"
    _many = namedtuple("Contacts", [_root_key, "has_more", "cursor"])

    class _Schema(Schema):
        uuid = fields.String()
        customer_uuid = fields.String(allow_none=True)
        data_source_uuid = fields.String(allow_none=True)
        customer_external_id = fields.String(allow_none=True)
        first_name = fields.String(allow_none=True)
        last_name = fields.String(allow_none=True)
        position = fields.Int(allow_none=True)
        email = fields.String(allow_none=True)
        title = fields.String(allow_none=True)
        notes = fields.String(allow_none=True)
        phone = fields.String(allow_none=True)
        linked_in = fields.String(allow_none=True)
        twitter = fields.String(allow_none=True)
        # load_default=None ensures this attribute is always present on the Contact
        # object even when the API omits the field (e.g. older responses)
        external_id = fields.String(allow_none=True, load_default=None)
        last_seen = fields.DateTime(allow_none=True)
        custom = fields.Dict(allow_none=True)

        @post_load
        def make(self, data, **kwargs):
            return Contact(**data)

    _schema = _Schema(unknown=EXCLUDE)


Contact.merge = Contact._method("merge", "post", "/contacts/{into_uuid}/merge/{from_uuid}")
Contact.tasks = Task._method("all", "get", "/tasks?contact_uuid={uuid}", useCallerClass=True)
Contact.createTask = Task._method(
    "create", "post", "/tasks", useCallerClass=True,
    useAssociatedObjectFor=ASSOCIATED_OBJECT_CONTACT
)
Contact.entityNotes = EntityNote._method(
    "all", "get", "/notes?contact_uuid={uuid}", useCallerClass=True
)
Contact.createEntityNote = EntityNote._method(
    "create", "post", "/notes", useCallerClass=True,
    useAssociatedObjectFor=ASSOCIATED_OBJECT_CONTACT
)
