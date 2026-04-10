import unittest

import requests_mock

from chartmogul import CustomAttributes, Config


class CustomAttrsByEmailTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_add_by_email(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/customers/attributes/custom",
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
                        "attributes": {"custom": {"plan": "enterprise"}},
                    }
                ]
            },
        )

        config = Config("token")
        result = CustomAttributes.add_by_email(
            config,
            data={
                "email": "test@example.com",
                "custom": [{"key": "plan", "value": "enterprise"}],
            },
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(len(result.entries), 1)
