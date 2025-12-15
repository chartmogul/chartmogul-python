import unittest

from chartmogul import DataSource, Config, APIError, ArgumentMissingError
from datetime import datetime
import requests_mock
from pprint import pprint
from collections import namedtuple


class DataSourceTestCase(unittest.TestCase):
    """
    Tests basic CRUD ops, schema mapping.
    """

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/data_sources",
            status_code=200,
            json={
                "name": "test",
                "uuid": "my_uuid",
                "created_at": "2016-01-10T15:34:05.144Z",
                "status": "idle",
            },
        )

        config = Config("token")
        ds = DataSource.create(config, data={"name": "test"}).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), {"name": "test"})
        # Direct comparison impossible because of tzinfo difference between 2.7 and 3.3+
        self.assertTrue(isinstance(ds, DataSource))
        self.assertTrue(isinstance(ds.created_at, datetime))
        self.assertEqual(ds.uuid, "my_uuid")

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/data_sources/my_uuid",
            status_code=200,
            json={
                "name": "test",
                "uuid": "my_uuid",
                "created_at": "2016-01-10T15:34:05Z",
                "status": "idle",
                "processing_status": {
                    "processed": 61,
                    "failed": 3,
                    "pending": 8
                },
                "auto_churn_subscription_setting": {
                    "enabled": True,
                    "interval": 30
                },
                "invoice_handling_setting": {
                    "manual": {
                        "create_subscription_when_invoice_is": "open",
                        "update_subscription_when_invoice_is": "open",
                        "prevent_subscription_for_invoice_voided": True,
                        "prevent_subscription_for_invoice_refunded": False,
                        "prevent_subscription_for_invoice_written_off": True
                    },
                    "automatic": {
                        "create_subscription_when_invoice_is": "open",
                        "update_subscription_when_invoice_is": "open",
                        "prevent_subscription_for_invoice_voided": True,
                        "prevent_subscription_for_invoice_refunded": False,
                        "prevent_subscription_for_invoice_written_off": True
                    }
                }
            },
        )

        config = Config("token")
        ds = DataSource.retrieve(
            config,
            uuid="my_uuid",
            with_processing_status=True,
            with_auto_churn_subscription_setting=True,
            with_invoice_handling_setting=True
        ).get()
        expected = DataSource(
            **{
                "name": "test",
                "uuid": "my_uuid",
                "created_at": datetime(2016, 1, 10, 15, 34, 5),
                "status": "idle",
                "processing_status": {
                    "processed": 61,
                    "failed": 3,
                    "pending": 8
                },
                "auto_churn_subscription_setting": {
                    "enabled": True,
                    "interval": 30
                },
                "invoice_handling_setting": {
                    "manual": {
                        "create_subscription_when_invoice_is": "open",
                        "update_subscription_when_invoice_is": "open",
                        "prevent_subscription_for_invoice_voided": True,
                        "prevent_subscription_for_invoice_refunded": False,
                        "prevent_subscription_for_invoice_written_off": True
                    },
                    "automatic": {
                        "create_subscription_when_invoice_is": "open",
                        "update_subscription_when_invoice_is": "open",
                        "prevent_subscription_for_invoice_voided": True,
                        "prevent_subscription_for_invoice_refunded": False,
                        "prevent_subscription_for_invoice_written_off": True
                    }
                }
            }
        )

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {
            "with_processing_status": ["true"],
            "with_auto_churn_subscription_setting": ["true"],
            "with_invoice_handling_setting": ["true"]
        })
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertTrue(isinstance(ds, DataSource))
        self.assertTrue(isinstance(ds.created_at, datetime))
        self.assertEqual(ds.name, "test")
        self.assertEqual(ds.processing_status.processed, 61)
        self.assertEqual(ds.auto_churn_subscription_setting.interval, 30)
        self.assertEqual(ds.invoice_handling_setting['manual']['create_subscription_when_invoice_is'], "open")

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/data_sources",
            status_code=200,
            json={
                "data_sources": [
                    {
                        "name": "test",
                        "uuid": "my_uuid",
                        "created_at": "2016-01-10T15:34:05Z",
                        "status": "idle",
                        "processing_status": {
                            "processed": 61,
                            "failed": 3,
                            "pending": 8
                        },
                        "auto_churn_subscription_setting": {
                            "enabled": True,
                            "interval": 30
                        },
                        "invoice_handling_setting": {
                            "manual": {
                                "create_subscription_when_invoice_is": "open",
                                "update_subscription_when_invoice_is": "open",
                                "prevent_subscription_for_invoice_voided": True,
                                "prevent_subscription_for_invoice_refunded": False,
                                "prevent_subscription_for_invoice_written_off": True
                            },
                            "automatic": {
                                "create_subscription_when_invoice_is": "open",
                                "update_subscription_when_invoice_is": "open",
                                "prevent_subscription_for_invoice_voided": True,
                                "prevent_subscription_for_invoice_refunded": False,
                                "prevent_subscription_for_invoice_written_off": True
                            }
                        }
                    }
                ]
            },
        )

        config = Config("token")
        ds = DataSource.all(
            config,
            with_processing_status=True,
            with_auto_churn_subscription_setting=True,
            with_invoice_handling_setting=True
        ).get()
        expected = DataSource._many(
            data_sources=[
                DataSource(
                    **{
                        "name": "test",
                        "uuid": "my_uuid",
                        "created_at": datetime(2016, 1, 10, 15, 34, 5),
                        "status": "idle",
                        "processing_status": {
                            "processed": 61,
                            "failed": 3,
                            "pending": 8
                        },
                        "auto_churn_subscription_setting": {
                            "enabled": True,
                            "interval": 30
                        },
                        "invoice_handling_setting": {
                            "manual": {
                                "create_subscription_when_invoice_is": "open",
                                "update_subscription_when_invoice_is": "open",
                                "prevent_subscription_for_invoice_voided": True,
                                "prevent_subscription_for_invoice_refunded": False,
                                "prevent_subscription_for_invoice_written_off": True
                            },
                            "automatic": {
                                "create_subscription_when_invoice_is": "open",
                                "update_subscription_when_invoice_is": "open",
                                "prevent_subscription_for_invoice_voided": True,
                                "prevent_subscription_for_invoice_refunded": False,
                                "prevent_subscription_for_invoice_written_off": True
                            }
                        }
                    }
                )
            ]
        )

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {
            "with_processing_status": ["true"],
            "with_auto_churn_subscription_setting": ["true"],
            "with_invoice_handling_setting": ["true"]
        })
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertTrue(isinstance(ds.data_sources[0], DataSource))
        self.assertTrue(isinstance(ds.data_sources[0].created_at, datetime))
        self.assertEqual(ds.data_sources[0].name, "test")
        self.assertEqual(ds.data_sources[0].processing_status.processed, 61)
        self.assertEqual(ds.data_sources[0].auto_churn_subscription_setting.interval, 30)
        self.assertEqual(ds.data_sources[0].invoice_handling_setting['manual']['create_subscription_when_invoice_is'], "open")

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE", "https://api.chartmogul.com/v1/data_sources/my_uuid", status_code=204
        )

        config = Config("token")
        res = DataSource.destroy(config, uuid="my_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(res, None)
