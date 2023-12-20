import unittest
from chartmogul import CustomerNote, Config
import requests_mock

from pprint import pprint

note = {
    "uuid": "note_00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "type": "note",
    "text": "This is a note",
    "call_duration": 0,
    "author": "John Doe (john@example.com)",
    "created_at": "2015-06-09T13:16:00-04:00",
    "updated_at": "2015-06-09T13:16:00-04:00"
}

createNote = {
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "type": "note",
    "text": "This is a note",
    "author_email": "john@example.com"
}

allNotes = {"entries": [note], "cursor": "cursor==", "has_more": False}


class CustomerNoteTestCase(unittest.TestCase):
    """
    Tests complex nested structure & assymetric create/retrieve schema.
    """

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customer_notes?cursor=ym9vewfo&per_page=1&customer_uuid=cus_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=allNotes,
        )

        config = Config("token")
        notes = CustomerNote.all(
            config,
            customer_uuid="cus_00000000-0000-0000-0000-000000000000",
            cursor="ym9vewfo",
            per_page=1,
        ).get()
        expected = CustomerNote._many(**allNotes)

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
        self.assertTrue(isinstance(notes.entries[0], CustomerNote))
        self.assertFalse(notes.has_more)
        self.assertEqual(notes.cursor, "cursor==")

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/customer_notes", status_code=200, json=note
        )

        config = Config("token")
        expected = CustomerNote.create(config, data=createNote).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createNote)
        self.assertTrue(expected, note)

    @requests_mock.mock()
    def test_patch(self, mock_requests):
        new_note = {
            "uuid": "note_00000000-0000-0000-0000-000000000000",
            "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
            "type": "note",
            "text": "new text",
            "call_duration": 0,
            "author": "John Doe (john@example.com')"
        }
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/customer_notes/note_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=new_note,
        )

        new_text = {"text": "new text"}

        config = Config("token")
        expected = CustomerNote.patch(
            config, uuid="note_00000000-0000-0000-0000-000000000000", data=new_text
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), new_text)
        self.assertTrue(isinstance(expected, CustomerNote))

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customer_notes/note_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=note,
        )

        config = Config("token")
        expected = CustomerNote.retrieve(
            config, uuid="note_00000000-0000-0000-0000-000000000000"
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(expected, CustomerNote))

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/customer_notes/note_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json={},
        )

        config = Config("token")
        expected = CustomerNote.destroy(
            config, uuid="note_00000000-0000-0000-0000-000000000000"
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(expected, {})
