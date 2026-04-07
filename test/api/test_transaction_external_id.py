import unittest

import requests_mock

from chartmogul import Transaction, Config, APIError


transaction_response = {
    "uuid": "tr_test",
    "external_id": "tr_ext_1",
    "type": "payment",
    "date": "2025-11-05T00:04:03.000Z",
    "result": "successful",
    "amount_in_cents": 5000,
    "disabled": False,
}


class TransactionExternalIdTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_retrieve_by_external_id(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/transactions"
            "?data_source_uuid=ds_123&external_id=tr_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=transaction_response,
        )

        config = Config("token")
        result = Transaction.retrieve_by_external_id(
            config, data_source_uuid="ds_123", external_id="tr_ext_1"
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertIn("data_source_uuid", mock_requests.last_request.qs)
        self.assertIn("external_id", mock_requests.last_request.qs)
        self.assertTrue(isinstance(result, Transaction))
        self.assertEqual(result.uuid, "tr_test")

    @requests_mock.mock()
    def test_update_by_external_id(self, mock_requests):
        updated = dict(transaction_response)
        updated["amount_in_cents"] = 10000

        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/transactions"
            "?data_source_uuid=ds_123&external_id=tr_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=updated,
        )

        config = Config("token")
        result = Transaction.update_by_external_id(
            config,
            data_source_uuid="ds_123",
            external_id="tr_ext_1",
            data={"amount_in_cents": 10000},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(mock_requests.last_request.json(), {"amount_in_cents": 10000})
        self.assertTrue(isinstance(result, Transaction))

    @requests_mock.mock()
    def test_update_by_external_id_with_handle_as_user_edit(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/transactions"
            "?data_source_uuid=ds_123&external_id=tr_ext_1&handle_as_user_edit=true",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=transaction_response,
        )

        config = Config("token")
        Transaction.update_by_external_id(
            config,
            data_source_uuid="ds_123",
            external_id="tr_ext_1",
            handle_as_user_edit=True,
            data={"amount_in_cents": 5000},
        ).get()

        self.assertEqual(
            mock_requests.last_request.qs["handle_as_user_edit"], ["true"]
        )

    @requests_mock.mock()
    def test_destroy_by_external_id(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/transactions"
            "?data_source_uuid=ds_123&external_id=tr_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
        )

        config = Config("token")
        result = Transaction.destroy_by_external_id(
            config, data_source_uuid="ds_123", external_id="tr_ext_1"
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_toggle_disabled_by_external_id(self, mock_requests):
        disabled = dict(transaction_response)
        disabled["disabled"] = True

        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/transactions/disabled_state"
            "?data_source_uuid=ds_123&external_id=tr_ext_1",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=disabled,
        )

        config = Config("token")
        result = Transaction.toggle_disabled_by_external_id(
            config,
            data_source_uuid="ds_123",
            external_id="tr_ext_1",
            data={"disabled": True},
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(mock_requests.last_request.json(), {"disabled": True})
        self.assertTrue(isinstance(result, Transaction))
        self.assertTrue(result.disabled)

    @requests_mock.mock()
    def test_destroy_by_external_id_not_found(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/transactions"
            "?data_source_uuid=ds_123&external_id=tr_bad",
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=404,
            json={"error": "Transaction not found"},
        )

        config = Config("token")
        with self.assertRaises(APIError):
            Transaction.destroy_by_external_id(
                config, data_source_uuid="ds_123", external_id="tr_bad"
            ).get()
