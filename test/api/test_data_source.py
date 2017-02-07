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
            'POST',
            "https://api.chartmogul.com/v1/data_sources",
            status_code=200,
            json={"name": "test", "uuid": "my_uuid",
                  "created_at": "2016-01-10 15:34:05", "status": "never_imported"}
        )

        config = Config("token", "secret")
        ds = DataSource.create(config, data={"name": "test"}).get()
        expected = DataSource(**{"name": u"test",
                                 "uuid": u"my_uuid",
                                 "created_at": datetime(2016, 1, 10, 15, 34, 5),
                                 "status": u"never_imported"})
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), {"name": "test"})
        self.assertEqual(str(ds), str(expected))

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/data_sources/my_uuid",
            status_code=200,
            json={"name": "test",
                  "uuid": "my_uuid",
                  "created_at": "2016-01-10 15:34:05",
                  "status": "never_imported"}
        )

        config = Config("token", "secret")
        ds = DataSource.retrieve(config, uuid="my_uuid").get()
        expected = DataSource(**{"name": u"test",
                                 "uuid": u"my_uuid",
                                 "created_at": datetime(2016, 1, 10, 15, 34, 5),
                                 "status": u"never_imported"})

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(ds), str(expected))

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/data_sources",
            status_code=200,
            json={"data_sources": [
                {"name": "test",
                 "uuid": "my_uuid",
                 "created_at": "2016-01-10 15:34:05",
                 "status": "never_imported"}
            ]}
        )

        config = Config("token", "secret")
        ds = DataSource.all(config).get()
        expected = DataSource._many(data_sources=[
            DataSource(**{"name": u"test",
                          "uuid": u"my_uuid",
                          "created_at": datetime(2016, 1, 10, 15, 34, 5),
                          "status": u"never_imported"})])

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(ds), str(expected))

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            'DELETE',
            "https://api.chartmogul.com/v1/data_sources/my_uuid",
            status_code=204
        )

        config = Config("token", "secret")
        res = DataSource.destroy(config, uuid="my_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(res, None)
