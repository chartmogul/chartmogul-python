import unittest

import requests_mock

from chartmogul import LineItem, Config, APIError


line_item_response = {
    "uuid": "li_test",
    "external_id": "li_ext_1",
    "type": "subscription",
    "amount_in_cents": 5000,
    "quantity": 1,
    "discount_amount_in_cents": 0,
    "tax_amount_in_cents": 0,
    "transaction_fees_in_cents": 0,
    "prorated": False,
    "disabled": False,
}


class LineItemTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/line_items"
            "?data_source_uuid=ds_123&external_id=li_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=line_item_response,
        )

        config = Config("token")
        result = LineItem.retrieve(
            config, data_source_uuid="ds_123", external_id="li_ext_1"
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIn("data_source_uuid", mock_requests.last_request.qs)
        self.assertIn("external_id", mock_requests.last_request.qs)
        self.assertIsInstance(result, LineItem)
        self.assertEqual(result.uuid, "li_test")

    @requests_mock.mock()
    def test_modify(self, mock_requests):
        updated = dict(line_item_response)
        updated["amount_in_cents"] = 10000

        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/line_items"
            "?data_source_uuid=ds_123&external_id=li_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=updated,
        )

        config = Config("token")
        result = LineItem.modify(
            config,
            data_source_uuid="ds_123",
            external_id="li_ext_1",
            data={"amount_in_cents": 10000},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(mock_requests.last_request.json(), {"amount_in_cents": 10000})
        self.assertIsInstance(result, LineItem)
        self.assertEqual(result.amount_in_cents, 10000)

    @requests_mock.mock()
    def test_modify_with_handle_as_user_edit(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/line_items"
            "?data_source_uuid=ds_123&external_id=li_ext_1&handle_as_user_edit=true",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=line_item_response,
        )

        config = Config("token")
        LineItem.modify(
            config,
            data_source_uuid="ds_123",
            external_id="li_ext_1",
            handle_as_user_edit=True,
            data={"amount_in_cents": 5000},
        ).get()

        self.assertEqual(
            mock_requests.last_request.qs["handle_as_user_edit"], ["true"]
        )

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/line_items"
            "?data_source_uuid=ds_123&external_id=li_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
        )

        config = Config("token")
        result = LineItem.destroy(
            config, data_source_uuid="ds_123", external_id="li_ext_1"
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIsNone(result)

    @requests_mock.mock()
    def test_disable(self, mock_requests):
        disabled = dict(line_item_response)
        disabled["disabled"] = True

        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/line_items/disabled_state"
            "?data_source_uuid=ds_123&external_id=li_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=disabled,
        )

        config = Config("token")
        result = LineItem.disable(
            config,
            data_source_uuid="ds_123",
            external_id="li_ext_1",
            data={"disabled": True},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(mock_requests.last_request.json(), {"disabled": True})
        self.assertIsInstance(result, LineItem)
        self.assertTrue(result.disabled)

    @requests_mock.mock()
    def test_retrieve_by_uuid(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/line_items/li_test",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=line_item_response,
        )

        config = Config("token")
        result = LineItem.retrieve(config, uuid="li_test").get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIsInstance(result, LineItem)
        self.assertEqual(result.uuid, "li_test")

    @requests_mock.mock()
    def test_modify_by_uuid(self, mock_requests):
        updated = dict(line_item_response)
        updated["amount_in_cents"] = 10000

        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/line_items/li_test",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=updated,
        )

        config = Config("token")
        result = LineItem.modify(
            config, uuid="li_test", data={"amount_in_cents": 10000}
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIsInstance(result, LineItem)
        self.assertEqual(result.amount_in_cents, 10000)

    @requests_mock.mock()
    def test_destroy_by_uuid(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/line_items/li_test",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
        )

        config = Config("token")
        result = LineItem.destroy(config, uuid="li_test").get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIsNone(result)

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/import/invoices/inv_123/line_items",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=line_item_response,
        )

        config = Config("token")
        result = LineItem.create(
            config,
            uuid="inv_123",
            data={"type": "subscription", "amount_in_cents": 5000},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIsInstance(result, LineItem)

    @requests_mock.mock()
    def test_disable_by_uuid(self, mock_requests):
        disabled = dict(line_item_response)
        disabled["disabled"] = True

        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/line_items/li_test/disabled_state",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=disabled,
        )

        config = Config("token")
        result = LineItem.disable(
            config, uuid="li_test", data={"disabled": True}
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIsInstance(result, LineItem)
        self.assertTrue(result.disabled)

    @requests_mock.mock()
    def test_retrieve_not_found(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/line_items"
            "?data_source_uuid=ds_123&external_id=li_bad",
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=404,
            json={"error": "Line item not found"},
        )

        config = Config("token")
        with self.assertRaises(APIError):
            LineItem.retrieve(
                config, data_source_uuid="ds_123", external_id="li_bad"
            ).get()
