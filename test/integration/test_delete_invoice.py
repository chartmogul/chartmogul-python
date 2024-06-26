import unittest
from datetime import datetime
from promise import Promise

import requests_mock
from chartmogul import DataSource, Customer, Plan, Config, Invoice

config = Config("-")


def _create_plan(ds):
    customer = Customer.create(
        config,
        data={
            "data_source_uuid": ds.uuid,
            "external_id": "cus_0001",
            "name": "Adam Smith",
            "email": "adam@smith.com",
            "country": "US",
            "city": "New York",
        },
    )
    plan = Plan.create(
        config,
        data={
            "data_source_uuid": ds.uuid,
            "name": "Bronze Plan",
            "interval_count": 1,
            "interval_unit": "month",
            "external_id": "plan_0001",
        },
    )
    return Promise.all([ds.uuid, customer, plan])


def _create_invoice(result):
    ds_uuid, customer, plan = result
    return Invoice.create(
        config,
        uuid=customer.uuid,
        data={
            "invoices": [
                {
                    "external_id": "INV0001",
                    "date": datetime(2015, 11, 1, 0, 0, 0),
                    "currency": "USD",
                    "due_date": datetime(2015, 11, 15, 0, 0, 0),
                    "line_items": [
                        {
                            "type": "subscription",
                            "subscription_external_id": "sub_0001",
                            "plan_uuid": plan.uuid,
                            "service_period_start": datetime(2015, 11, 1, 0, 0, 0),
                            "service_period_end": datetime(2015, 12, 1, 0, 0, 0),
                            "amount_in_cents": 5000,
                            "quantity": 1,
                            "discount_code": "PSO86",
                            "discount_amount_in_cents": 1000,
                            "tax_amount_in_cents": 900,
                        }
                    ],
                    "transactions": [
                        {
                            "date": datetime(2015, 11, 5, 0, 14, 23),
                            "type": "payment",
                            "result": "successful",
                        }
                    ],
                }
            ]
        },
    )


def _delete_invoice(result):
    return Invoice.destroy(config, uuid=result.invoices[0].uuid)


class DeleteInvoiceTestCase(unittest.TestCase):
    """
    Tests deleting an invoice.
    """

    @requests_mock.Mocker()
    def test_delete_invoice(self, m):
        # Mock DataSource.create
        m.post(
            "https://api.chartmogul.com/v1/data_sources",
            json={
                "uuid": "ds_20b98cde-565d-11e7-953a-57e7aa662af2",
                "name": "Test",
                "system": "Import API",
                "created_at": "2017-06-21T08:39:23.884Z",
                "status": "idle",
            },
            status_code=201,
        )

        # Mock Customer.create
        m.post(
            "https://api.chartmogul.com/v1/customers",
            json={
                "id": 9232806,
                "uuid": "cus_20fdab30-565d-11e7-953a-c3eecbf6873c",
                "external_id": "cus_0001",
                "name": "Adam Smith",
                "email": "adam@smith.com",
                "status": "Lead",
                "data_source_uuid": "ds_20b98cde-565d-11e7-953a-57e7aa662af2",
                "country": "US",
                "city": "New York",
            },
            status_code=201,
        )

        # Mock Plan.create
        m.post(
            "https://api.chartmogul.com/v1/plans",
            json={
                "external_id": "plan_0001",
                "name": "Bronze Plan",
                "interval_count": 1,
                "interval_unit": "month",
                "data_source_uuid": "ds_20b98cde-565d-11e7-953a-57e7aa662af2",
                "uuid": "pl_21436c24-565d-11e7-99b5-c30bc3e995a3",
            },
            status_code=201,
        )

        # Mock Invoice.create
        m.post(
            "https://api.chartmogul.com/v1/import/customers/cus_20fdab30-565d-11e7-953a-c3eecbf6873c/invoices",
            json={
                "invoices": [
                    {
                        "uuid": "inv_fb369587-7ed5-4049-9f02-8f6a8000499c",
                        "external_id": "INV0001",
                        "date": "2015-11-01T00:00:00.000Z",
                        "due_date": "2015-11-15T00:00:00.000Z",
                        "currency": "USD",
                        "line_items": [
                            {
                                "uuid": "li_1421544c-04bc-49f8-819c-8d37fe0bea9f",
                                "type": "subscription",
                                "subscription_uuid": "sub_81a2a3b2-94f1-4858-94ea-852d9487acad",
                                "subscription_external_id": "sub_0001",
                                "plan_uuid": "pl_21436c24-565d-11e7-99b5-c30bc3e995a3",
                                "service_period_start": "2015-11-01T00:00:00.000Z",
                                "service_period_end": "2015-12-01T00:00:00.000Z",
                                "amount_in_cents": 5000,
                                "quantity": 1,
                                "discount_code": "PSO86",
                                "discount_amount_in_cents": 1000,
                                "tax_amount_in_cents": 900,
                            }
                        ],
                        "transactions": [
                            {
                                "uuid": "tr_a3d85ea1-7ae0-4a72-af28-3457993b3b4e",
                                "type": "payment",
                                "date": "2015-11-05T00:14:23.000Z",
                                "result": "successful",
                            }
                        ],
                    }
                ]
            },
            status_code=201,
        )

        # Mock Invoice.destroy
        m.delete(
            "https://api.chartmogul.com/v1/invoices/inv_fb369587-7ed5-4049-9f02-8f6a8000499c",
            status_code=204,
        )

        # Execute the chain of promises and get the result
        result = (
            DataSource.create(config, data={"name": "Test"})
            .then(_create_plan)
            .then(_create_invoice)
            .then(_delete_invoice)
            .get()
        )

        # Assertions
        # Ensure that the DataSource, Customer, and Plan were created with the correct UUIDs
        ds_result = DataSource.create(config, data={"name": "Test"}).get()
        self.assertEqual(ds_result.uuid, "ds_20b98cde-565d-11e7-953a-57e7aa662af2")

        customer_result = Customer.create(
            config,
            data={
                "data_source_uuid": ds_result.uuid,
                "external_id": "cus_0001",
                "name": "Adam Smith",
                "email": "adam@smith.com",
                "country": "US",
                "city": "New York",
            },
        ).get()
        self.assertEqual(
            customer_result.uuid, "cus_20fdab30-565d-11e7-953a-c3eecbf6873c"
        )

        plan_result = Plan.create(
            config,
            data={
                "data_source_uuid": ds_result.uuid,
                "name": "Bronze Plan",
                "interval_count": 1,
                "interval_unit": "month",
                "external_id": "plan_0001",
            },
        ).get()
        self.assertEqual(plan_result.uuid, "pl_21436c24-565d-11e7-99b5-c30bc3e995a3")

        # Ensure that the invoice was created correctly
        invoice_creation_result = Invoice.create(
            config,
            uuid=customer_result.uuid,
            data={
                "invoices": [
                    {
                        "external_id": "INV0001",
                        "date": datetime(2015, 11, 1, 0, 0, 0),
                        "currency": "USD",
                        "due_date": datetime(2015, 11, 15, 0, 0, 0),
                        "line_items": [
                            {
                                "type": "subscription",
                                "subscription_external_id": "sub_0001",
                                "plan_uuid": plan_result.uuid,
                                "service_period_start": datetime(2015, 11, 1, 0, 0, 0),
                                "service_period_end": datetime(2015, 12, 1, 0, 0, 0),
                                "amount_in_cents": 5000,
                                "quantity": 1,
                                "discount_code": "PSO86",
                                "discount_amount_in_cents": 1000,
                                "tax_amount_in_cents": 900,
                            }
                        ],
                        "transactions": [
                            {
                                "date": datetime(2015, 11, 5, 0, 14, 23),
                                "type": "payment",
                                "result": "successful",
                            }
                        ],
                    }
                ]
            },
        ).get()
        self.assertEqual(
            invoice_creation_result.invoices[0].uuid,
            "inv_fb369587-7ed5-4049-9f02-8f6a8000499c",
        )

        # Ensure that the invoice was deleted
        deletion_result = Invoice.destroy(
            config, uuid=invoice_creation_result.invoices[0].uuid
        )
        self.assertIsNone(deletion_result.get())
