import unittest
from datetime import date, datetime

import requests_mock
from requests.exceptions import HTTPError

from chartmogul import (
    DataSource,
    Config,
    APIError,
    ArgumentMissingError,
    DeprecatedArgumentError,
)


class CommonTestCase(unittest.TestCase):
    """
    Tests errors & user mistakes.
    """

    @requests_mock.mock()
    def test_forget_uuid_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/data_sources/my_uuid",
            status_code=204,
        )
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/data_sources",
            status_code=404,
            text="Not found",
        )

        config = Config("token")
        try:
            res = DataSource.destroy(config).get()
        except ArgumentMissingError:
            pass
        else:
            self.fail("ArgumentMissingError not raised")

    @requests_mock.mock()
    def test_forget_uuid_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/data_sources",
            status_code=200,
            json={
                "data_sources": [
                    {
                        "name": "test",
                        "uuid": "my_uuid",
                        "created_at": "2016-01-10 15:34:05",
                        "status": "never_imported",
                    }
                ]
            },
        )

        config = Config("token")
        try:
            DataSource.retrieve(config).get()
        except ArgumentMissingError:
            pass
        else:
            self.fail("ArgumentMissingError not raised")

    @requests_mock.mock()
    def test_page_parameter_deprecated(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/data_sources?page=1",
            status_code=400,
            json={
                "code": 400,
                "message": 'Parameter "page" is deprecated',
                "param": "page",
            },
        )

        config = Config("token")
        try:
            DataSource.all(config, page=1).get()
        except DeprecatedArgumentError:
            pass
        else:
            self.fail("DeprecatedArgumentError not raised")

    @requests_mock.mock()
    def test_api_incorrect(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/data_sources",
            status_code=400,
            json={
                "code": 400,
                "message": 'Parameter "name" is missing',
                "param": "name",
            },
        )

        config = Config("token")
        try:
            DataSource.create(config, data={"xname": "abc"}).get()
        except APIError as err:
            self.assertTrue(isinstance(err.__cause__, HTTPError))
        else:
            self.fail("ArgumentMissingError not raised")

    @requests_mock.mock()
    def test_date_serialization(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/data_sources",
            status_code=200,  # whatever, not testing this
            json={"data_sources": []},
        )

        config = Config("token")

        DataSource.create(config, data={"test_date": date(2015, 1, 1)}).get()
        self.assertEqual(mock_requests.last_request.json(), {"test_date": "2015-01-01"})

        DataSource.create(config, data={"test_datetime": datetime(2015, 1, 1, 1, 2, 3)}).get()
        self.assertEqual(
            mock_requests.last_request.json(), {"test_datetime": "2015-01-01T01:02:03"}
        )
