import unittest

import requests_mock

from chartmogul import Invoice, Config, APIError


invoice_response = {
    "invoices": [
        {
            "uuid": "inv_test",
            "external_id": "inv_ext_1",
            "date": "2025-11-01T00:00:00.000Z",
            "due_date": "2025-11-15T00:00:00.000Z",
            "currency": "USD",
            "line_items": [],
            "transactions": [],
        }
    ],
    "cursor": None,
    "has_more": False,
}

single_invoice_response = {
    "uuid": "inv_test",
    "external_id": "inv_ext_1",
    "date": "2025-11-01T00:00:00.000Z",
    "due_date": "2025-11-15T00:00:00.000Z",
    "currency": "USD",
    "disabled": True,
    "line_items": [],
    "transactions": [],
}


class InvoiceExternalIdTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_retrieve_by_external_id(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/invoices"
            "?data_source_uuid=ds_123&external_id=inv_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=invoice_response,
        )

        config = Config("token")
        result = Invoice.retrieve_by_external_id(
            config, data_source_uuid="ds_123", external_id="inv_ext_1"
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIn("data_source_uuid", mock_requests.last_request.qs)
        self.assertIn("external_id", mock_requests.last_request.qs)

    @requests_mock.mock()
    def test_update_by_external_id(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/invoices"
            "?data_source_uuid=ds_123&external_id=inv_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=single_invoice_response,
        )

        config = Config("token")
        result = Invoice.update_by_external_id(
            config,
            data_source_uuid="ds_123",
            external_id="inv_ext_1",
            data={"currency": "EUR"},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIn("data_source_uuid", mock_requests.last_request.qs)
        self.assertEqual(mock_requests.last_request.json(), {"currency": "EUR"})

    @requests_mock.mock()
    def test_update_by_external_id_with_handle_as_user_edit(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/invoices"
            "?data_source_uuid=ds_123&external_id=inv_ext_1&handle_as_user_edit=true",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=single_invoice_response,
        )

        config = Config("token")
        result = Invoice.update_by_external_id(
            config,
            data_source_uuid="ds_123",
            external_id="inv_ext_1",
            handle_as_user_edit=True,
            data={"currency": "EUR"},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(
            mock_requests.last_request.qs["handle_as_user_edit"], ["true"]
        )

    @requests_mock.mock()
    def test_destroy_by_external_id(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/invoices"
            "?data_source_uuid=ds_123&external_id=inv_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
        )

        config = Config("token")
        result = Invoice.destroy_by_external_id(
            config, data_source_uuid="ds_123", external_id="inv_ext_1"
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIn("data_source_uuid", mock_requests.last_request.qs)
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_toggle_disabled_by_external_id(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/invoices/disabled_state"
            "?data_source_uuid=ds_123&external_id=inv_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=single_invoice_response,
        )

        config = Config("token")
        result = Invoice.toggle_disabled_by_external_id(
            config,
            data_source_uuid="ds_123",
            external_id="inv_ext_1",
            data={"disabled": True},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(mock_requests.last_request.json(), {"disabled": True})
        self.assertTrue(isinstance(result, Invoice))

    @requests_mock.mock()
    def test_destroy_by_external_id_not_found(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/invoices"
            "?data_source_uuid=ds_123&external_id=inv_bad",
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=404,
            json={"error": "Invoice not found"},
        )

        config = Config("token")
        with self.assertRaises(APIError):
            Invoice.destroy_by_external_id(
                config, data_source_uuid="ds_123", external_id="inv_bad"
            ).get()
