import unittest
from datetime import datetime, timezone

import requests_mock

from chartmogul import ExcludedCustomer, Config, APIError

allExcludedCustomers = {
    "entries": [
        {
            "customer_uuid": "cus_00000000-0000-0000-0000-000000000001",
            "data_source_uuid": "ds_00000000-0000-0000-0000-000000000001",
            "external_id": "ext-1",
            "name": "Acme",
            "email": "acme@example.com",
            "excluded_at": "2026-11-20T10:00:00.000Z",
        },
        {
            "customer_uuid": "cus_00000000-0000-0000-0000-000000000001",
            "data_source_uuid": "ds_00000000-0000-0000-0000-000000000002",
            "external_id": "ext-2",
            "name": "Acme",
            "email": None,
            "excluded_at": "2026-11-19T10:00:00.000Z",
        },
    ],
    "cursor": "cursor==",
    "has_more": True,
}


class ExcludedCustomerTestCase(unittest.TestCase):
    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/excluded_customers?cursor=prev%3D%3D&per_page=2",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=allExcludedCustomers,
        )

        config = Config("token")
        result = ExcludedCustomer.all(config, cursor="prev==", per_page=2).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs, {"cursor": ["prev=="], "per_page": ["2"]}
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(result.cursor, "cursor==")
        self.assertTrue(result.has_more)
        self.assertEqual(len(result.entries), 2)
        entry = result.entries[0]
        self.assertTrue(isinstance(entry, ExcludedCustomer))
        self.assertEqual(entry.customer_uuid, "cus_00000000-0000-0000-0000-000000000001")
        self.assertEqual(entry.data_source_uuid, "ds_00000000-0000-0000-0000-000000000001")
        self.assertEqual(entry.external_id, "ext-1")
        self.assertEqual(entry.name, "Acme")
        self.assertEqual(entry.email, "acme@example.com")
        self.assertEqual(entry.excluded_at, datetime(2026, 11, 20, 10, tzinfo=timezone.utc))
        self.assertIsNone(entry.status)
        self.assertEqual(result.entries[1].data_source_uuid, "ds_00000000-0000-0000-0000-000000000002")
        self.assertIsNone(result.entries[1].email)

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/excluded_customers/cus_00000000-0000-0000-0000-000000000001",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=202,
            json={
                "customer_uuid": "cus_00000000-0000-0000-0000-000000000001",
                "status": "reimporting",
            },
        )

        config = Config("token")
        result = ExcludedCustomer.destroy(
            config, uuid="cus_00000000-0000-0000-0000-000000000001"
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertTrue(isinstance(result, ExcludedCustomer))
        self.assertEqual(result.customer_uuid, "cus_00000000-0000-0000-0000-000000000001")
        self.assertEqual(result.status, "reimporting")

    @requests_mock.mock()
    def test_destroy_not_excluded(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/excluded_customers/cus_00000000-0000-0000-0000-000000000001",
            status_code=404,
            json={"error": "Customer not found"},
        )

        config = Config("token")
        with self.assertRaises(APIError) as context:
            ExcludedCustomer.destroy(
                config, uuid="cus_00000000-0000-0000-0000-000000000001"
            ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertTrue("Customer not found" in str(context.exception))
