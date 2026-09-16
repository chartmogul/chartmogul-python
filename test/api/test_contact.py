import unittest
from datetime import datetime
from chartmogul import Contact, Config, EntityNote, Task
import requests_mock

from pprint import pprint

contact = {
    "uuid": "con_00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "data_source_uuid": "ds_00000000-0000-0000-0000-000000000000",
    "customer_external_id": "external_001",
    "external_id": "contact_external_id_001",
    "first_name": "First name",
    "last_name": "Last name",
    "position": 9,
    "title": "Title",
    "email": "test@example.com",
    "phone": "+1234567890",
    "linked_in": "https://linkedin.com/not_found",
    "twitter": "https://twitter.com/not_found",
    "notes": "Heading\nBody\nFooter",
    "last_seen": "2025-04-01T12:00:00Z",
    "custom": {"MyStringAttribute": "Test", "MyIntegerAttribute": 123},
}

createContact = {
    "uuid": "con_00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "data_source_uuid": "ds_00000000-0000-0000-0000-000000000000",
    "external_id": "contact_external_id_001",
    "first_name": "First name",
    "last_name": "Last name",
    "position": 9,
    "title": "Title",
    "email": "test@example.com",
    "phone": "+1234567890",
    "linked_in": "https://linkedin.com/not_found",
    "twitter": "https://twitter.com/not_found",
    "notes": "Heading\nBody\nFooter",
    "custom": [
        {"key": "MyStringAttribute", "value": "Test"},
        {"key": "MyIntegerAttribute", "value": 123},
    ],
}

allContacts = {"entries": [contact], "cursor": "cursor==", "has_more": False}

contactWithoutExternalId = {k: v for k, v in contact.items() if k != "external_id"}

contactWithNullExternalId = {
    **contact,
    "external_id": None,
}

createContactWithNullExternalId = {
    **createContact,
    "external_id": None,
}

standaloneContact = {
    **contact,
    "customer_uuid": None,
    "customer_external_id": None,
    "data_source_uuid": None,
}

createStandaloneContact = {
    k: v for k, v in createContact.items()
    if k not in ("uuid", "customer_uuid", "data_source_uuid")
}

contactTask = {
    "task_uuid": "00000000-0000-0000-0000-000000000000",
    "customer_uuid": None,
    "associated_object": "contact",
    "associated_object_uuid": "con_00000000-0000-0000-0000-000000000000",
    "assignee": "customer@example.com",
    "task_details": "This is some task details text.",
    "due_date": "2025-04-30T00:00:00Z",
    "completed_at": None,
    "created_at": "2025-04-01T12:00:00.000Z",
    "updated_at": "2025-04-01T12:00:00.000Z",
}

createContactTask = {
    "assignee": "customer@example.com",
    "task_details": "This is some task details text.",
    "due_date": "2025-04-30T00:00:00Z",
}

contactAssociatedObjectIdentifier = {
    "associated_object": "contact",
    "method": "uuid",
    "value": "con_00000000-0000-0000-0000-000000000000",
}

allContactTasks = {"entries": [contactTask], "cursor": "cursor==", "has_more": False}

contactNote = {
    "uuid": "note_00000000-0000-0000-0000-000000000000",
    "customer_uuid": None,
    "associated_object": "contact",
    "associated_object_uuid": "con_00000000-0000-0000-0000-000000000000",
    "type": "note",
    "text": "This is a note",
    "call_duration": 0,
    "author": "John Doe (john@example.com)",
    "created_at": "2015-06-09T13:16:00-04:00",
    "updated_at": "2015-06-09T13:16:00-04:00",
}

createContactNote = {
    "type": "note",
    "text": "This is a note",
    "author_email": "john@example.com",
}

allContactNotes = {"entries": [contactNote], "cursor": "cursor==", "has_more": False}


class ContactTestCase(unittest.TestCase):
    """
    Tests complex nested structure & assymetric create/retrieve schema.
    """

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/contacts?cursor=Ym9veWFo&per_page=1&data_source_uuid=ds_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=allContacts,
        )

        config = Config("token")
        contacts = Contact.all(
            config,
            data_source_uuid="ds_00000000-0000-0000-0000-000000000000",
            cursor="Ym9veWFo",
            per_page=1,
        ).get()
        expected = Contact._many(**allContacts)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "cursor": ["ym9vewfo"],
                "per_page": ["1"],
                "data_source_uuid": ["ds_00000000-0000-0000-0000-000000000000"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(dir(contacts), dir(expected))
        self.assertTrue(isinstance(contacts.entries[0], Contact))
        self.assertFalse(contacts.has_more)
        self.assertEqual(contacts.cursor, "cursor==")

    @requests_mock.mock()
    def test_all_with_filters(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/contacts?customer_uuid=cus_00000000-0000-0000-0000-000000000000&data_source_uuid=ds_00000000-0000-0000-0000-000000000000&email=test@example.com&customer_external_id=external_001&external_id=contact_external_id_001",
            status_code=200,
            json=allContacts,
        )

        config = Config("token")
        Contact.all(
            config,
            customer_uuid="cus_00000000-0000-0000-0000-000000000000",
            data_source_uuid="ds_00000000-0000-0000-0000-000000000000",
            email="test@example.com",
            customer_external_id="external_001",
            external_id="contact_external_id_001",
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "customer_uuid": ["cus_00000000-0000-0000-0000-000000000000"],
                "data_source_uuid": ["ds_00000000-0000-0000-0000-000000000000"],
                "email": ["test@example.com"],
                "customer_external_id": ["external_001"],
                "external_id": ["contact_external_id_001"],
            },
        )

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/contacts", status_code=200, json=contact
        )

        config = Config("token")
        Contact.create(config, data=createContact).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createContact)

    @requests_mock.mock()
    def test_create_with_null_external_id(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/contacts", status_code=200, json=contactWithNullExternalId
        )

        config = Config("token")
        result = Contact.create(config, data=createContactWithNullExternalId).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.json(), createContactWithNullExternalId)
        self.assertIsNone(result.external_id)

    @requests_mock.mock()
    def test_create_without_external_id(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/contacts", status_code=200, json=contactWithoutExternalId
        )

        config = Config("token")
        result = Contact.create(config, data=createContactWithNullExternalId).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.json(), createContactWithNullExternalId)
        self.assertIsNone(result.external_id)

    @requests_mock.mock()
    def test_create_standalone(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/contacts", status_code=200, json=standaloneContact
        )

        config = Config("token")
        result = Contact.create(config, data=createStandaloneContact).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.json(), createStandaloneContact)
        self.assertIsNone(result.customer_uuid)
        self.assertIsNone(result.data_source_uuid)

    @requests_mock.mock()
    def test_merge(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000/merge/con_00000000-0000-0000-0000-000000000001",
            status_code=200,
            json=contact,
        )

        config = Config("token")
        expected = Contact.merge(
            config,
            into_uuid="con_00000000-0000-0000-0000-000000000000",
            from_uuid="con_00000000-0000-0000-0000-000000000001",
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(expected, Contact))

    @requests_mock.mock()
    def test_modify(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=contact,
        )

        jsonRequest = {"email": "test2@example.com"}
        config = Config("token")
        expected = Contact.modify(
            config, uuid="con_00000000-0000-0000-0000-000000000000", data=jsonRequest
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), jsonRequest)
        self.assertTrue(isinstance(expected, Contact))

    @requests_mock.mock()
    def test_modify_with_null_external_id(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=contactWithNullExternalId,
        )

        jsonRequest = {"external_id": None}
        config = Config("token")
        result = Contact.modify(
            config, uuid="con_00000000-0000-0000-0000-000000000000", data=jsonRequest
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.json(), jsonRequest)
        self.assertIsNone(result.external_id)

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=contact,
        )

        config = Config("token")
        expected = Contact.retrieve(config, uuid="con_00000000-0000-0000-0000-000000000000").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(expected, Contact))
        self.assertEqual(expected.email, "test@example.com")
        self.assertTrue(isinstance(expected.last_seen, datetime))

    @requests_mock.mock()
    def test_tasks(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/tasks?contact_uuid=con_00000000-0000-0000-0000-000000000000&cursor=df431387&per_page=1",
            status_code=200,
            json=allContactTasks,
        )

        config = Config("token")
        tasks = Contact.tasks(
            config,
            uuid="con_00000000-0000-0000-0000-000000000000",
            cursor="df431387",
            per_page=1,
        ).get()
        expected = Task._many(**allContactTasks)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "contact_uuid": ["con_00000000-0000-0000-0000-000000000000"],
                "cursor": ["df431387"],
                "per_page": ["1"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(sorted(dir(tasks)), sorted(dir(expected)))
        self.assertTrue(isinstance(tasks.entries[0], Task))
        self.assertIsNone(tasks.entries[0].customer_uuid)
        self.assertEqual(tasks.cursor, "cursor==")
        self.assertFalse(tasks.has_more)

    @requests_mock.mock()
    def test_createTask(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/tasks", status_code=200, json=contactTask
        )

        config = Config("token")
        result = Contact.createTask(
            config, uuid="con_00000000-0000-0000-0000-000000000000", data=dict(createContactTask)
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(
            mock_requests.last_request.json(),
            {**createContactTask, "associated_object_identifier": contactAssociatedObjectIdentifier},
        )
        self.assertTrue(isinstance(result, Task))
        self.assertEqual(result.associated_object, "contact")

    @requests_mock.mock()
    def test_createTask_with_customer_uuid(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/tasks", status_code=200, json=contactTask
        )

        data = {**createContactTask, "customer_uuid": "cus_00000000-0000-0000-0000-000000000000"}
        config = Config("token")
        Contact.createTask(
            config, uuid="con_00000000-0000-0000-0000-000000000000", data=data
        ).get()

        self.assertEqual(mock_requests.last_request.json(), data)
        self.assertNotIn("associated_object_identifier", mock_requests.last_request.json())

    @requests_mock.mock()
    def test_createTask_with_explicit_identifier(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/tasks", status_code=200, json=contactTask
        )

        explicit_identifier = {
            "associated_object": "customer",
            "method": "uuid",
            "value": "cus_00000000-0000-0000-0000-000000000000",
        }
        data = {**createContactTask, "associated_object_identifier": explicit_identifier}
        config = Config("token")
        Contact.createTask(
            config, uuid="con_00000000-0000-0000-0000-000000000000", data=data
        ).get()

        self.assertEqual(
            mock_requests.last_request.json()["associated_object_identifier"], explicit_identifier
        )

    @requests_mock.mock()
    def test_entityNotes(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/notes?contact_uuid=con_00000000-0000-0000-0000-000000000000&cursor=ym9vewfo&per_page=1",
            status_code=200,
            json=allContactNotes,
        )

        config = Config("token")
        notes = Contact.entityNotes(
            config,
            uuid="con_00000000-0000-0000-0000-000000000000",
            cursor="ym9vewfo",
            per_page=1,
        ).get()
        expected = EntityNote._many(**allContactNotes)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "contact_uuid": ["con_00000000-0000-0000-0000-000000000000"],
                "cursor": ["ym9vewfo"],
                "per_page": ["1"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(sorted(dir(notes)), sorted(dir(expected)))
        self.assertTrue(isinstance(notes.entries[0], EntityNote))
        self.assertIsNone(notes.entries[0].customer_uuid)
        self.assertEqual(notes.cursor, "cursor==")
        self.assertFalse(notes.has_more)

    @requests_mock.mock()
    def test_createEntityNote(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/notes", status_code=200, json=contactNote
        )

        config = Config("token")
        result = Contact.createEntityNote(
            config, uuid="con_00000000-0000-0000-0000-000000000000", data=dict(createContactNote)
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(
            mock_requests.last_request.json(),
            {**createContactNote, "associated_object_identifier": contactAssociatedObjectIdentifier},
        )
        self.assertTrue(isinstance(result, EntityNote))
        self.assertEqual(result.associated_object, "contact")

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json={},
        )

        config = Config("token")
        expected = Contact.destroy(config, uuid="con_00000000-0000-0000-0000-000000000000").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(expected, {})
