# pylama:ignore=W0212
import unittest
from datetime import datetime

import requests_mock

from chartmogul import Config
from chartmogul.imp import Invoice


requestData = {
    "invoices": [
        {
            "external_id": "INV0001",
            "date": datetime(2015, 11, 1, 0, 0, 0),  # "2015-11-01 00:00:00",
            "currency": "USD",
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
                    "tax_amount_in_cents": 900
                },
                {
                    "type": "one_time",
                    "description": "Setup Fees",
                    "amount_in_cents": 2500,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 500,
                    "tax_amount_in_cents": 450
                }
            ],
            "transactions": [
                {
                    # "2015-11-05 00:14:23",
                    "date": datetime(2015, 11, 5, 0, 4, 3),
                    "type": "payment",
                    "result": "successful"
                }
            ]
        }
    ]
}

requestSerialized = {
    u"invoices": [
        {
            u"external_id": u"INV0001",
            u"date": u"2015-11-01T00:00:00",
            u"currency": u"USD",
            u"due_date": u"2015-11-15T00:00:00",
            u"line_items": [
                {
                    u"type": "subscription",
                    u"subscription_external_id": "sub_0001",
                    u"plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                    u"service_period_start": "2015-11-01T00:00:00",
                    u"service_period_end": "2015-12-01T00:00:00",
                    u"amount_in_cents": 5000,
                    u"quantity": 1,
                    u"discount_code": "PSO86",
                    u"discount_amount_in_cents": 1000,
                    u"tax_amount_in_cents": 900
                },
                {
                    "type": "one_time",
                    "description": "Setup Fees",
                    "amount_in_cents": 2500,
                    "quantity": 1,
                    "discount_code": "PSO86",
                    "discount_amount_in_cents": 500,
                    "tax_amount_in_cents": 450
                }
            ],
            "transactions": [
                {
                    "date": "2015-11-05T00:04:03",
                    "type": "payment",
                    "result": "successful"
                }
            ]
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
                    "account_code": None
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
                    "account_code": None
                }
            ],
            "transactions": [
                {
                    "uuid": "tr_879d560a-1bec-41bb-986e-665e38a2f7bc",
                    "external_id": None,
                    "type": "payment",
                    "date": "2015-11-05T00:04:03.000Z",
                    "result": "successful"
                }
            ]
        }
    ]
}


class InvoiceTestCase(unittest.TestCase):
    """
    Tests most important Import API part and its nested schemas.
    """
    maxDiff = None

    @requests_mock.mock()
    def test_create(self, mock_requests):

        mock_requests.register_uri(
            'POST',
            "https://api.chartmogul.com/v1/import/customers/UUID/invoices",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json=responseData
        )

        config = Config("token", "secret")  # is actually checked in mock
        result = Invoice.create(config, uuid="UUID", data=requestData).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), requestSerialized)
        # Struct too complex to do 1:1 comparison
        self.assertTrue(isinstance(result, Invoice._many))
        self.assertEqual(len(result.invoices), 1)
