import unittest
import vcr
from datetime import date, datetime
from promise import Promise

import requests_mock
from requests.exceptions import HTTPError

from chartmogul import DataSource, Customer, Plan, Config, Invoice

config = Config('-')

def _create_plan(ds):
    customer = Customer.create(config, data={
        "data_source_uuid": ds.uuid,
        "external_id": "cus_0001",
        "name": "Adam Smith",
        "email": "adam@smith.com",
        "country": "US",
        "city": "New York"
    })
    plan = Plan.create(config, data={
        "data_source_uuid": ds.uuid,
        "name": "Bronze Plan",
        "interval_count": 1,
        "interval_unit": "month",
        "external_id": "plan_0001"
    })
    return Promise.all([ds.uuid, customer, plan])

def _create_invoice(result):
    ds_uuid, customer, plan = result
    return Invoice.create(
    config,
    uuid=customer.uuid,
    data={
        "invoices": [{
            "external_id": "INV0001",
            "date": datetime(2015, 11, 1, 0, 0, 0),
            "currency": "USD",
            "due_date": datetime(2015, 11, 15, 0, 0, 0),
            "line_items": [{
                "type": "subscription",
                "subscription_external_id": "sub_0001",
                "plan_uuid": plan.uuid,
                "service_period_start": datetime(2015, 11, 1, 0, 0, 0),
                "service_period_end": datetime(2015, 12, 1, 0, 0, 0),
                "amount_in_cents": 5000,
                "quantity": 1,
                "discount_code": "PSO86",
                "discount_amount_in_cents": 1000,
                "tax_amount_in_cents": 900
            }],
            "transactions": [{
                "date": datetime(2015, 11, 5, 0, 14, 23),
                "type": "payment",
                "result": "successful"
            }]
        }]
    })

def _delete_invoice(result):
    return Invoice.destroy(config, uuid=result.invoices[0].uuid)

class DeleteInvoiceTestCase(unittest.TestCase):
    """
    Tests errors & user mistakes.
    """
    @vcr.use_cassette('fixtures/delete_invoice.yaml', filter_headers=['authorization'])
    def test_delete_invoice(self):
        result = (
            DataSource.create(
              	config, data={'name': 'Test'}
            )
            .then(_create_plan)
            .then(_create_invoice)
            .then(_delete_invoice)
            .get()
        )
        print(result)
