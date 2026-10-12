import unittest
from chartmogul import EntityNote, Config
import requests_mock

note = {
    "uuid": "note_00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "associated_object": "customer",
    "associated_object_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "type": "note",
    "text": "This is a note",
    "call_duration": 0,
    "author": "John Doe (john@example.com)",
    "created_at": "2015-06-09T13:16:00-04:00",
    "updated_at": "2015-06-09T13:16:00-04:00"
}

contactNote = {
    "uuid": "note_00000000-0000-0000-0000-000000000001",
    "customer_uuid": None,
    "associated_object": "contact",
    "associated_object_uuid": "con_00000000-0000-0000-0000-000000000000",
    "type": "call",
    "text": "This is a call log",
    "call_duration": 60,
    "author": "John Doe (john@example.com)",
    "created_at": "2015-06-09T13:16:00-04:00",
    "updated_at": "2015-06-09T13:16:00-04:00"
}

noteWithoutAssociatedObject = {
    k: v for k, v in note.items()
    if k not in ("associated_object", "associated_object_uuid")
}

createNote = {
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "type": "note",
    "text": "This is a note",
    "author_email": "john@example.com"
}

createContactNote = {
    "associated_object_identifier": {
        "associated_object": "contact",
        "method": "uuid",
        "value": "con_00000000-0000-0000-0000-000000000000",
    },
    "type": "call",
    "text": "This is a call log",
    "call_duration": 60,
    "author_email": "john@example.com"
}

allNotes = {"entries": [note], "cursor": "cursor==", "has_more": False}
allContactNotes = {"entries": [contactNote], "cursor": "cursor==", "has_more": False}


class EntityNoteTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/notes?cursor=ym9vewfo&per_page=1&customer_uuid=cus_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=allNotes,
        )

        config = Config("token")
        notes = EntityNote.all(
            config,
            customer_uuid="cus_00000000-0000-0000-0000-000000000000",
            cursor="ym9vewfo",
            per_page=1,
        ).get()
        expected = EntityNote._many(**allNotes)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "cursor": ["ym9vewfo"],
                "per_page": ["1"],
                "customer_uuid": ["cus_00000000-0000-0000-0000-000000000000"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(dir(notes), dir(expected))
        self.assertTrue(isinstance(notes.entries[0], EntityNote))
        self.assertEqual(notes.entries[0].associated_object, "customer")
        self.assertFalse(notes.has_more)
        self.assertEqual(notes.cursor, "cursor==")

    @requests_mock.mock()
    def test_all_with_contact_filters(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/notes?contact_uuid=con_00000000-0000-0000-0000-000000000000&type=call&author_email=john@example.com",
            status_code=200,
            json=allContactNotes,
        )

        config = Config("token")
        notes = EntityNote.all(
            config,
            contact_uuid="con_00000000-0000-0000-0000-000000000000",
            type="call",
            author_email="john@example.com",
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "contact_uuid": ["con_00000000-0000-0000-0000-000000000000"],
                "type": ["call"],
                "author_email": ["john@example.com"],
            },
        )
        self.assertIsNone(notes.entries[0].customer_uuid)
        self.assertEqual(notes.entries[0].associated_object, "contact")
        self.assertEqual(
            notes.entries[0].associated_object_uuid, "con_00000000-0000-0000-0000-000000000000"
        )

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/notes", status_code=200, json=note
        )

        config = Config("token")
        result = EntityNote.create(config, data=createNote).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createNote)
        self.assertTrue(isinstance(result, EntityNote))
        self.assertEqual(result.uuid, note["uuid"])

    @requests_mock.mock()
    def test_create_with_associated_object_identifier(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/notes", status_code=200, json=contactNote
        )

        config = Config("token")
        result = EntityNote.create(config, data=createContactNote).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.json(), createContactNote)
        self.assertTrue(isinstance(result, EntityNote))
        self.assertIsNone(result.customer_uuid)
        self.assertEqual(result.associated_object, "contact")

    @requests_mock.mock()
    def test_patch(self, mock_requests):
        new_note = {**note, "text": "new text"}
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/notes/note_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=new_note,
        )

        new_text = {"text": "new text"}

        config = Config("token")
        result = EntityNote.patch(
            config, uuid="note_00000000-0000-0000-0000-000000000000", data=new_text
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), new_text)
        self.assertTrue(isinstance(result, EntityNote))
        self.assertEqual(result.text, "new text")

    @requests_mock.mock()
    def test_patch_not_modified(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/notes/note_00000000-0000-0000-0000-000000000000",
            status_code=304,
        )

        config = Config("token")
        result = EntityNote.patch(
            config, uuid="note_00000000-0000-0000-0000-000000000000", data={}
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(result, None)

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/notes/note_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=note,
        )

        config = Config("token")
        result = EntityNote.retrieve(
            config, uuid="note_00000000-0000-0000-0000-000000000000"
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(result, EntityNote))
        self.assertEqual(result.customer_uuid, "cus_00000000-0000-0000-0000-000000000000")

    @requests_mock.mock()
    def test_retrieve_without_associated_object(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/notes/note_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=noteWithoutAssociatedObject,
        )

        config = Config("token")
        result = EntityNote.retrieve(
            config, uuid="note_00000000-0000-0000-0000-000000000000"
        ).get()

        self.assertTrue(isinstance(result, EntityNote))
        self.assertIsNone(result.associated_object)
        self.assertIsNone(result.associated_object_uuid)

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/notes/note_00000000-0000-0000-0000-000000000000",
            status_code=202,
            json={"message": "Note has been deleted."},
        )

        config = Config("token")
        result = EntityNote.destroy(
            config, uuid="note_00000000-0000-0000-0000-000000000000"
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result, None)
