# pylama:ignore=W0212
import unittest
from datetime import datetime

import requests_mock

from requests.exceptions import HTTPError

from chartmogul import Config
from chartmogul import APIError
from chartmogul import Invoice


requestData = {
    "invoices": [
        {
            "external_id": "INV0001",
            "date": datetime(2015, 11, 1, 0, 0, 0),  # "2015-11-01 00:00:00",
            "currency": "USD",
            "customer_external_id": "ext-id",
            # "2015-11-15 00:00:00",
            "due_date": datetime(2015, 11, 15, 0, 0, 0),
            "line_items": [
                {
                    "type": "subscription",
                    "subscription_external_id": "sub_0001",
                    "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                    # "2015-11-01 00:00:00",
                    "service_period_start": datetime(2015, 11, 1, 0, 0, 0),
                    # "2015-12-01 00:00:00",
                    "service_period_end": datetime(2015, 12, 1, 0, 0, 0),
                    "amount_in_cents": 5000,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 1000,
                    "tax_amount_in_cents": 900,
                },
                {
                    "type": "one_time",
                    "description": "Setup Fees",
                    "amount_in_cents": 2500,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 500,
                    "tax_amount_in_cents": 450,
                    "discount_description": "Special 20 % discount",
                    "transaction_fees_in_cents": 50,
                    "transaction_fees_currency": "CZK",
                    "event_order": 5,
                },
            ],
            "transactions": [
                {
                    # "2015-11-05 00:14:23",
                    "date": datetime(2015, 11, 5, 0, 4, 3),
                    "type": "payment",
                    "result": "successful",
                    "amount_in_cents": 7500,
                }
            ],
        }
    ]
}

requestSerialized = {
    "invoices": [
        {
            "external_id": "INV0001",
            "date": "2015-11-01T00:00:00",
            "currency": "USD",
            "due_date": "2015-11-15T00:00:00",
            "customer_external_id": "ext-id",
            "line_items": [
                {
                    "type": "subscription",
                    "subscription_external_id": "sub_0001",
                    "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                    "service_period_start": "2015-11-01T00:00:00",
                    "service_period_end": "2015-12-01T00:00:00",
                    "amount_in_cents": 5000,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 1000,
                    "tax_amount_in_cents": 900,
                },
                {
                    "type": "one_time",
                    "description": "Setup Fees",
                    "amount_in_cents": 2500,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 500,
                    "tax_amount_in_cents": 450,
                    "discount_description": "Special 20 % discount",
                    "transaction_fees_in_cents": 50,
                    "transaction_fees_currency": "CZK",
                    "event_order": 5,
                },
            ],
            "transactions": [
                {
                    "date": "2015-11-05T00:04:03",
                    "type": "payment",
                    "result": "successful",
                    "amount_in_cents": 7500,
                }
            ],
        }
    ]
}

responseData = {
    "invoices": [
        {
            "uuid": "inv_565c73b2-85b9-49c9-a25e-2b7df6a677c9",
            "external_id": "INV0001",
            "date": "2015-11-01T00:00:00.000Z",
            "due_date": "2015-11-15T00:00:00.000Z",
            "currency": "USD",
            "line_items": [
                {
                    "uuid": "li_d72e6843-5793-41d0-bfdf-0269514c9c56",
                    "external_id": None,
                    "type": "subscription",
                    "subscription_uuid": "sub_e6bc5407-e258-4de0-bb43-61faaf062035",
                    "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                    "prorated": False,
                    "service_period_start": "2015-11-01T00:00:00.000Z",
                    "service_period_end": "2015-12-01T00:00:00.000Z",
                    "amount_in_cents": 5000,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 1000,
                    "tax_amount_in_cents": 900,
                    "account_code": None,
                },
                {
                    "uuid": "li_0cc8c112-beac-416d-af11-f35744ca4e83",
                    "external_id": None,
                    "type": "one_time",
                    "description": "Setup Fees",
                    "amount_in_cents": 2500,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 500,
                    "tax_amount_in_cents": 450,
                    "account_code": None,
                    "plan_uuid": None,
                    "discount_description": "Special 20 % discount",
                    "transaction_fees_in_cents": 50,
                    "transaction_fees_currency": "CZK",
                    "event_order": 5,
                },
            ],
            "transactions": [
                {
                    "uuid": "tr_879d560a-1bec-41bb-986e-665e38a2f7bc",
                    "external_id": None,
                    "type": "payment",
                    "date": "2015-11-05T00:04:03.000Z",
                    "result": "successful",
                    "amount_in_cents": 7500,
                }
            ],
        }
    ]
}

invoiceListExample = {
    "invoices": [
        {
            "uuid": "inv_565c73b2-85b9-49c9-a25e-2b7df6a677c9",
            "customer_uuid": "cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
            "external_id": "INV0001",
            "date": "2015-11-01T00:00:00.000Z",
            "due_date": "2015-11-15T00:00:00.000Z",
            "currency": "USD",
            "line_items": [
                {
                    "uuid": "li_d72e6843-5793-41d0-bfdf-0269514c9c56",
                    "external_id": None,
                    "type": "subscription",
                    "subscription_uuid": "sub_e6bc5407-e258-4de0-bb43-61faaf062035",
                    "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                    "prorated": False,
                    "service_period_start": "2015-11-01T00:00:00.000Z",
                    "service_period_end": "2015-12-01T00:00:00.000Z",
                    "amount_in_cents": 5000,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 1000,
                    "tax_amount_in_cents": 900,
                    "account_code": None,
                },
                {
                    "uuid": "li_0cc8c112-beac-416d-af11-f35744ca4e83",
                    "external_id": None,
                    "type": "one_time",
                    "description": "Setup Fees",
                    "amount_in_cents": 2500,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 500,
                    "tax_amount_in_cents": 450,
                    "account_code": None,
                    "discount_description": "Special 20 % discount",
                    "transaction_fees_in_cents": 50,
                    "transaction_fees_currency": "CZK",
                    "event_order": 5,
                },
            ],
            "transactions": [
                {
                    "uuid": "tr_879d560a-1bec-41bb-986e-665e38a2f7bc",
                    "external_id": None,
                    "type": "payment",
                    "date": "2015-11-05T00:14:23.000Z",
                    "result": "successful",
                }
            ],
        }
    ],
    "cursor": "cursor==",
    "has_more": False,
}


retrieveInvoiceExample = {
    "uuid": "inv_22910fc6-c931-48e7-ac12-90d2cb5f0059",
    "external_id": "INV0001",
    "date": "2015-11-01T00:00:00.000Z",
    "due_date": "2015-11-15T00:00:00.000Z",
    "currency": "USD",
    "line_items": [
        {
            "uuid": "li_d72e6843-5793-41d0-bfdf-0269514c9c56",
            "external_id": None,
            "type": "subscription",
            "subscription_uuid": "sub_e6bc5407-e258-4de0-bb43-61faaf062035",
            "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
            "prorated": False,
            "service_period_start": "2015-11-01T00:00:00.000Z",
            "service_period_end": "2015-12-01T00:00:00.000Z",
            "amount_in_cents": 5000,
            "quantity": 1,
            "discount_code": "PSO86",
            "discount_amount_in_cents": 1000,
            "tax_amount_in_cents": 900,
            "account_code": None,
        },
        {
            "uuid": "li_0cc8c112-beac-416d-af11-f35744ca4e83",
            "external_id": None,
            "type": "one_time",
            "description": "Setup Fees",
            "amount_in_cents": 2500,
            "quantity": 1,
            "discount_code": "PSO86",
            "discount_amount_in_cents": 500,
            "tax_amount_in_cents": 450,
            "account_code": None,
            "discount_description": "Special 20 % discount",
            "transaction_fees_in_cents": 50,
            "transaction_fees_currency": "CZK",
            "event_order": 5,
        },
    ],
    "transactions": [
        {
            "uuid": "tr_879d560a-1bec-41bb-986e-665e38a2f7bc",
            "external_id": None,
            "type": "payment",
            "date": "2015-11-05T00:14:23.000Z",
            "result": "successful",
        }
    ],
}


class InvoiceTestCase(unittest.TestCase):
    """
    Tests most important Import API part and its nested schemas.
    """

    maxDiff = None

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/import/customers/UUID/invoices",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=responseData,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.create(config, uuid="UUID", data=requestData).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), requestSerialized)
        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice._many))
        self.assertEqual(len(result.invoices), 1)

    @requests_mock.mock()
    def test_list_has_customer_uuid(self, mock_requests):
        responseData["customer_uuid"] = "UUID"
        responseData["cursor"] = None
        responseData["has_more"] = False

        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/import/customers/UUID/invoices",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=responseData,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.all(config, uuid="UUID").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice._many))
        self.assertEqual(len(result.invoices), 1)
        self.assertTrue(isinstance(result.invoices[0], Invoice))
        self.assertEqual(result.invoices[0].uuid, "inv_565c73b2-85b9-49c9-a25e-2b7df6a677c9")
        self.assertEqual(result.customer_uuid, "UUID")
        self.assertEqual(result.cursor, None)
        self.assertFalse(result.has_more)

    @requests_mock.mock()
    def test_new_list_old_pagination(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            (
                "https://api.chartmogul.com/v1/invoices"
                "?external_id=INV0001&customer_uuid=cus_f466e33d-ff2b-4a11-8f85-417eb02157a7"
            ),
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            json=invoiceListExample,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.all(
            config,
            customer_uuid="cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
            external_id="INV0001",
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        cu = []
        cu.append("cus_f466e33d-ff2b-4a11-8f85-417eb02157a7")
        ei = []
        ei.append("inv0001")
        self.assertEqual(mock_requests.last_request.qs, {"customer_uuid": cu, "external_id": ei})
        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice._many))
        self.assertEqual(len(result.invoices), 1)

        self.assertEqual(
            result.invoices[0].customer_uuid, "cus_f466e33d-ff2b-4a11-8f85-417eb02157a7"
        )
        self.assertEqual(result.cursor, "cursor==")
        self.assertFalse(result.has_more)

    @requests_mock.mock()
    def test_delete(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            ("https://api.chartmogul.com/v1/invoices" "/inv_f466e33d-ff2b-4a11-8f85-417eb02157a7"),
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.destroy(config, uuid="inv_f466e33d-ff2b-4a11-8f85-417eb02157a7").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_delete_not_found(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            ("https://api.chartmogul.com/v1/invoices" "/inv_f466e33d-ff2b-4a11-8f85-417eb02157a7"),
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=404,
            json={"error": "Invoice not found"},
        )

        config = Config("token")  # is actually checked in mock
        with self.assertRaises(APIError) as context:
            result = Invoice.destroy(config, uuid="inv_f466e33d-ff2b-4a11-8f85-417eb02157a7").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")

    @requests_mock.mock()
    def test_delete_all(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            (
                "https://api.chartmogul.com/v1/data_sources"
                "/ds_f466e33d-ff2b-4a11-8f85-417eb02157a7/customers"
                "/cus_f466e33d-ff2b-4a11-8f85-417eb02157a7/invoices"
            ),
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=204,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.destroy_all(
            config,
            data_source_uuid="ds_f466e33d-ff2b-4a11-8f85-417eb02157a7",
            customer_uuid="cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_retrieve_invoice(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            ("https://api.chartmogul.com/v1/invoices/inv_22910fc6-c931-48e7-ac12-90d2cb5f0059"),
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            json=retrieveInvoiceExample,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.retrieve(config, uuid="inv_22910fc6-c931-48e7-ac12-90d2cb5f0059").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")

        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice))

        self.assertEqual(result.uuid, "inv_22910fc6-c931-48e7-ac12-90d2cb5f0059")

    @requests_mock.mock()
    def test_retrieve_invoice_with_validation_type(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            ("https://api.chartmogul.com/v1/invoices/inv_22910fc6-c931-48e7-ac12-90d2cb5f0059"
             "?validation_type=all"),
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            json=retrieveInvoiceExample,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.retrieve(
            config,
            uuid="inv_22910fc6-c931-48e7-ac12-90d2cb5f0059",
            validation_type="all"
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        vt = []
        vt.append("all")
        self.assertEqual(mock_requests.last_request.qs, {"validation_type": vt})

        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice))

        self.assertEqual(result.uuid, "inv_22910fc6-c931-48e7-ac12-90d2cb5f0059")

    @requests_mock.mock()
    def test_retrieve_invoice_with_all_params(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            ("https://api.chartmogul.com/v1/invoices/inv_22910fc6-c931-48e7-ac12-90d2cb5f0059"
             "?validation_type=invalid&include_edit_histories=true&with_disabled=false"),
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            json=retrieveInvoiceExample,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.retrieve(
            config,
            uuid="inv_22910fc6-c931-48e7-ac12-90d2cb5f0059",
            validation_type="invalid",
            include_edit_histories=True,
            with_disabled=False
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        qs = mock_requests.last_request.qs
        self.assertEqual(qs["validation_type"], ["invalid"])
        self.assertEqual(qs["include_edit_histories"], ["true"])
        self.assertEqual(qs["with_disabled"], ["false"])

        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice))

        self.assertEqual(result.uuid, "inv_22910fc6-c931-48e7-ac12-90d2cb5f0059")

    @requests_mock.mock()
    def test_all_invoices_with_validation_type(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/invoices?validation_type=all",
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            json=invoiceListExample,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.all(config, validation_type="all").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {"validation_type": ["all"]},
        )

        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice._many))
        self.assertEqual(len(result.invoices), 1)

    @requests_mock.mock()
    def test_all_invoices_with_all_params(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            ("https://api.chartmogul.com/v1/invoices"
             "?validation_type=valid&include_edit_histories=true&with_disabled=true"),
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            json=invoiceListExample,
        )

        config = Config("token")  # is actually checked in mock
        result = Invoice.all(
            config,
            validation_type="valid",
            include_edit_histories=True,
            with_disabled=True
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        qs = mock_requests.last_request.qs
        self.assertEqual(qs["validation_type"], ["valid"])
        self.assertEqual(qs["include_edit_histories"], ["true"])
        self.assertEqual(qs["with_disabled"], ["true"])

        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice._many))
        self.assertEqual(len(result.invoices), 1)
