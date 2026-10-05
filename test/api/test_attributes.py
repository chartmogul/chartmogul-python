import unittest
from chartmogul import Attributes, Config
import requests_mock

attributesResponse = {
    "tags": ["engage", "unit loss"],
    "stripe": {"uid": 7, "coupon": True},
    "custom": {"CAC": 213, "salesRep": "Gabi"},
    "overrides": {"custom": {"salesRep": True}},
    "historical_values": {
        "custom": {
            "salesRep": [
                {
                    "value": "Gabi",
                    "update_performed_at": "2026-01-01T16:58:58Z",
                    "update_performed_by": "adam@example.com",
                    "initial": False,
                }
            ]
        }
    },
}


class AttributesTestCase(unittest.TestCase):
    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        plainResponse = {key: attributesResponse[key] for key in ("tags", "stripe", "custom")}
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customers/CUSTOMER_UUID/attributes",
            status_code=200,
            json=plainResponse,
        )

        config = Config("token")
        result = Attributes.retrieve(config, uuid="CUSTOMER_UUID").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(result, Attributes))
        self.assertEqual(result.custom, attributesResponse["custom"])
        self.assertIsNone(result.overrides)
        self.assertIsNone(result.historical_values)

    @requests_mock.mock()
    def test_retrieve_with_overrides_and_history(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customers/CUSTOMER_UUID/attributes",
            status_code=200,
            json=attributesResponse,
        )

        config = Config("token")
        result = Attributes.retrieve(
            config,
            uuid="CUSTOMER_UUID",
            with_overrides=True,
            attributes_with_history="custom.salesrep",
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {"with_overrides": ["true"], "attributes_with_history": ["custom.salesrep"]},
        )
        self.assertTrue(isinstance(result, Attributes))
        self.assertEqual(result.custom, attributesResponse["custom"])
        self.assertEqual(result.overrides, attributesResponse["overrides"])
        self.assertEqual(result.historical_values, attributesResponse["historical_values"])
