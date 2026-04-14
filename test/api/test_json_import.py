import unittest

import requests_mock

from chartmogul import JsonImport, Config


importRequestData = {
    "external_id": "import_batch_2026_04",
    "customers": [
        {
            "external_id": "cus_acme_001",
            "name": "Acme Corp",
            "email": "billing@acme.com",
            "company": "Acme Corporation",
            "country": "US",
            "state": "US-CA",
            "city": "San Francisco",
            "zip": "94105",
            "lead_created_at": "2025-10-15T00:00:00Z",
            "free_trial_started_at": "2025-11-01T00:00:00Z",
        },
        {
            "external_id": "cus_globex_002",
            "name": "Globex Inc",
            "email": "accounts@globex.io",
            "company": "Globex Inc",
            "country": "DE",
            "city": "Berlin",
        },
    ],
    "plans": [
        {
            "name": "Professional Monthly",
            "external_id": "plan_pro_monthly",
            "interval_count": 1,
            "interval_unit": "month",
        },
        {
            "name": "Enterprise Annual",
            "external_id": "plan_ent_annual",
            "interval_count": 1,
            "interval_unit": "year",
        },
    ],
    "invoices": [
        {
            "external_id": "inv_2025_11_001",
            "customer_external_id": "cus_acme_001",
            "date": "2025-11-01T00:00:00Z",
            "due_date": "2025-12-01T00:00:00Z",
            "currency": "USD",
            "collection_method": "automatic",
        },
        {
            "external_id": "inv_2025_12_001",
            "customer_external_id": "cus_acme_001",
            "date": "2025-12-01T00:00:00Z",
            "due_date": "2026-01-01T00:00:00Z",
            "currency": "USD",
        },
        {
            "external_id": "inv_2025_11_002",
            "customer_external_id": "cus_globex_002",
            "date": "2025-11-15T00:00:00Z",
            "due_date": "2025-12-15T00:00:00Z",
            "currency": "EUR",
            "collection_method": "manual",
        },
    ],
    "line_items": [
        {
            "invoice_external_id": "inv_2025_11_001",
            "type": "subscription",
            "amount_in_cents": 9900,
            "quantity": 5,
            "plan_external_id": "plan_pro_monthly",
            "subscription_external_id": "sub_acme_pro",
            "service_period_start": "2025-11-01T00:00:00Z",
            "service_period_end": "2025-12-01T00:00:00Z",
        },
        {
            "invoice_external_id": "inv_2025_12_001",
            "type": "subscription",
            "amount_in_cents": 9900,
            "quantity": 5,
            "plan_external_id": "plan_pro_monthly",
            "subscription_external_id": "sub_acme_pro",
            "service_period_start": "2025-12-01T00:00:00Z",
            "service_period_end": "2026-01-01T00:00:00Z",
            "discount_amount_in_cents": 500,
            "discount_code": "WINTER25",
            "tax_amount_in_cents": 1700,
        },
        {
            "invoice_external_id": "inv_2025_11_002",
            "type": "subscription",
            "amount_in_cents": 249900,
            "quantity": 1,
            "plan_external_id": "plan_ent_annual",
            "subscription_external_id": "sub_globex_ent",
            "service_period_start": "2025-11-15T00:00:00Z",
            "service_period_end": "2026-11-15T00:00:00Z",
            "tax_amount_in_cents": 47481,
            "transaction_fees_in_cents": 7497,
            "transaction_fees_currency": "EUR",
        },
        {
            "invoice_external_id": "inv_2025_11_001",
            "type": "one_time",
            "amount_in_cents": 5000,
            "description": "Onboarding setup fee",
        },
    ],
    "transactions": [
        {
            "invoice_external_id": "inv_2025_11_001",
            "external_id": "txn_001",
            "type": "payment",
            "result": "successful",
            "date": "2025-11-01T12:30:00Z",
        },
        {
            "invoice_external_id": "inv_2025_12_001",
            "external_id": "txn_002",
            "type": "payment",
            "result": "successful",
            "date": "2025-12-01T08:15:00Z",
        },
        {
            "invoice_external_id": "inv_2025_11_002",
            "external_id": "txn_003",
            "type": "payment",
            "result": "successful",
            "date": "2025-11-16T10:00:00Z",
            "amount_in_cents": 249900,
        },
    ],
    "subscription_events": [
        {
            "external_id": "evt_acme_start",
            "customer_external_id": "cus_acme_001",
            "subscription_external_id": "sub_acme_pro",
            "plan_external_id": "plan_pro_monthly",
            "event_type": "subscription_start",
            "event_date": "2025-11-01T00:00:00Z",
            "effective_date": "2025-11-01T00:00:00Z",
            "currency": "USD",
            "amount_in_cents": 9900,
            "quantity": 5,
        },
        {
            "external_id": "evt_globex_start",
            "customer_external_id": "cus_globex_002",
            "subscription_external_id": "sub_globex_ent",
            "subscription_set_external_id": "set_globex_main",
            "plan_external_id": "plan_ent_annual",
            "event_type": "subscription_start",
            "event_date": "2025-11-15T00:00:00Z",
            "effective_date": "2025-11-15T00:00:00Z",
            "currency": "EUR",
            "amount_in_cents": 249900,
            "quantity": 1,
            "tax_amount_in_cents": 47481,
        },
    ],
}

importResponseData = {
    "id": "4815d987-abcd-11ee-a987-978df45c5114",
    "data_source_uuid": "ds_45d064ca-fcf8-11f0-903f-33618f80d753",
    "status": "queued",
    "external_id": "import_batch_2026_04",
    "status_details": {},
    "created_at": "2026-04-14T10:30:00Z",
    "updated_at": "2026-04-14T10:30:00Z",
}

importStatusResponseData = {
    "id": "4815d987-abcd-11ee-a987-978df45c5114",
    "data_source_uuid": "ds_45d064ca-fcf8-11f0-903f-33618f80d753",
    "status": "completed",
    "external_id": "import_batch_2026_04",
    "status_details": {
        "plans": {"status": "imported"},
        "cus_acme_001": {
            "status": "imported",
            "invoices": {"status": "imported"},
            "customers": {"status": "imported"},
            "line_items": {"status": "imported"},
            "transactions": {"status": "imported"},
            "subscription_events": {"status": "imported"},
        },
        "cus_globex_002": {
            "status": "imported",
            "invoices": {"status": "imported"},
            "customers": {"status": "imported"},
            "line_items": {"status": "imported"},
            "transactions": {"status": "imported"},
            "subscription_events": {"status": "imported"},
        },
    },
    "created_at": "2026-04-14T10:30:00Z",
    "updated_at": "2026-04-14T10:31:15Z",
}


class JsonImportTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/data_sources/ds_45d064ca-fcf8-11f0-903f-33618f80d753/json_imports",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=importResponseData,
        )

        config = Config("token")
        result = JsonImport.create(
            config,
            uuid="ds_45d064ca-fcf8-11f0-903f-33618f80d753",
            data=importRequestData,
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        sent = mock_requests.last_request.json()
        self.assertEqual(sent["external_id"], "import_batch_2026_04")
        self.assertEqual(len(sent["customers"]), 2)
        self.assertEqual(sent["customers"][0]["external_id"], "cus_acme_001")
        self.assertEqual(len(sent["plans"]), 2)
        self.assertEqual(sent["plans"][0]["interval_unit"], "month")
        self.assertEqual(len(sent["invoices"]), 3)
        self.assertEqual(len(sent["line_items"]), 4)
        self.assertEqual(len(sent["transactions"]), 3)
        self.assertEqual(len(sent["subscription_events"]), 2)

        self.assertTrue(isinstance(result, JsonImport))
        self.assertEqual(result.id, "4815d987-abcd-11ee-a987-978df45c5114")
        self.assertEqual(result.data_source_uuid, "ds_45d064ca-fcf8-11f0-903f-33618f80d753")
        self.assertEqual(result.status, "queued")
        self.assertEqual(result.external_id, "import_batch_2026_04")
        self.assertEqual(result.status_details, {})

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/data_sources/ds_45d064ca-fcf8-11f0-903f-33618f80d753/json_imports/4815d987-abcd-11ee-a987-978df45c5114",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=importStatusResponseData,
        )

        config = Config("token")
        result = JsonImport.retrieve(
            config,
            uuid="ds_45d064ca-fcf8-11f0-903f-33618f80d753",
            import_id="4815d987-abcd-11ee-a987-978df45c5114",
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertTrue(isinstance(result, JsonImport))
        self.assertEqual(result.id, "4815d987-abcd-11ee-a987-978df45c5114")
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.external_id, "import_batch_2026_04")
        self.assertEqual(result.status_details["plans"]["status"], "imported")
        self.assertEqual(
            result.status_details["cus_acme_001"]["invoices"]["status"], "imported"
        )
