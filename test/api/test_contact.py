import unittest
from chartmogul import Contact, Config
import requests_mock

from pprint import pprint

contact = {
    "uuid": "con_00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "data_source_uuid": "ds_00000000-0000-0000-0000-000000000000",
    "customer_external_id": "external_001",
    "first_name": "First name",
    "last_name": "Last name",
    "position": 9,
    "title": "Title",
    "email": "test@example.com",
    "phone": "+1234567890",
    "linked_in": "https://linkedin.com/not_found",
    "twitter": "https://twitter.com/not_found",
    "notes": "Heading\nBody\nFooter",
    "custom": {
      "MyStringAttribute": "Test",
      "MyIntegerAttribute": 123
    }
}

createContact = {
    "uuid": "con_00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "data_source_uuid": "ds_00000000-0000-0000-0000-000000000000",
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
      { "key": "MyStringAttribute", "value": "Test" },
      { "key": "MyIntegerAttribute", "value": 123 }
    ]
}

allContacts = {
    "entries": [contact],
    "cursor": "MjAyMy0wMy0xMFQwMzo1MzoxNS44MTg1MjUwMDArMDA6MDAmY29uXzE2NDcwZjk4LWJlZjctMTFlZC05MjA4LTdiMDhhNDBmMzA0OQ==",
    "has_more": False
}


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
            json=allContacts
        )

        config = Config("token")
        contacts = Contact.all(config, data_source_uuid="ds_00000000-0000-0000-0000-000000000000", cursor="Ym9veWFo", per_page=1).get()
        expected = Contact._many(**allContacts)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {
          "cursor": ["ym9vewfo"],
          "per_page": ["1"],
          "data_source_uuid": ["ds_00000000-0000-0000-0000-000000000000"]
        })
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(dir(contacts), dir(expected))
        self.assertTrue(isinstance(contacts.entries[0], Contact))

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/contacts",
            status_code=200,
            json=contact
        )

        config = Config("token")
        Contact.create(config, data=createContact).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createContact)

    @requests_mock.mock()
    def test_merge(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000/merge/con_00000000-0000-0000-0000-000000000001",
            status_code=200,
            json=contact
        )

        config = Config("token")
        expected = Contact.merge(config, into_uuid="con_00000000-0000-0000-0000-000000000000", from_uuid="con_00000000-0000-0000-0000-000000000001").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(expected, Contact))

    @requests_mock.mock()
    def test_modify(self, mock_requests):
       mock_requests.register_uri(
           "PATCH",
           "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000",
           status_code=200,
           json=contact
       )

       jsonRequest = {
         "email": "test2@example.com"
       }
       config = Config("token")
       expected = Contact.modify(config, uuid="con_00000000-0000-0000-0000-000000000000", data=jsonRequest).get()

       self.assertEqual(mock_requests.call_count, 1, "expected call")
       self.assertEqual(mock_requests.last_request.qs, {})
       self.assertEqual(mock_requests.last_request.json(), jsonRequest)
       self.assertTrue(isinstance(expected, Contact))

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=contact
        )

        config = Config("token")
        expected = Contact.retrieve(config, uuid="con_00000000-0000-0000-0000-000000000000").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(expected, Contact))

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/contacts/con_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json={}
        )

        config = Config("token")
        expected = Contact.destroy(config, uuid="con_00000000-0000-0000-0000-000000000000").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(expected, {})
