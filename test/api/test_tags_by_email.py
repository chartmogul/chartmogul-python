import unittest

import requests_mock

from chartmogul import Tags, Config


class TagsByEmailTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_add_by_email(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/customers/attributes/tags",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json={
                "entries": [
                    {
                        "id": 1,
                        "uuid": "cus_test",
                        "external_id": "ext_1",
                        "name": "Test Customer",
                        "email": "test@example.com",
                        "data_source_uuid": "ds_1",
                        "status": "Active",
                        "customer-since": "2025-01-01T00:00:00.000Z",
                        "attributes": {"tags": ["important"]},
                    }
                ]
            },
        )

        config = Config("token")
        result = Tags.add_by_email(
            config,
            data={"email": "test@example.com", "tags": ["important"]},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(
            mock_requests.last_request.json(),
            {"email": "test@example.com", "tags": ["important"]},
        )
        self.assertEqual(len(result.entries), 1)
