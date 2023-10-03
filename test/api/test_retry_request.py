import unittest

import httpretty
import chartmogul
from chartmogul import Config, DataSource
from datetime import date, datetime
from requests.exceptions import RetryError
from chartmogul.retry_request import requests_retry_session


class RetryRequestTestCase(unittest.TestCase):
    @httpretty.activate
    def test_retry_request(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://example:444/testing",
            responses=[
                httpretty.Response(body="{}", status=500),
                httpretty.Response(body="{}", status=200),
            ],
        )

        with self.assertRaises(RetryError):
            requests_retry_session(0).get("https://example:444/testing")

        response = requests_retry_session(2, 0).get("https://example:444/testing")
        self.assertEqual(response.text, "{}")

    @httpretty.activate
    def test_requests_retry_session_on_resource(self):
        httpretty.register_uri(
            httpretty.POST,
            "https://api.chartmogul.com/v1/data_sources",
            responses=[
                httpretty.Response(body="{}", status=500),
                httpretty.Response(body="{}", status=500),
                httpretty.Response(body="{}", status=500),
                httpretty.Response(body="{}", status=500),
                httpretty.Response(body="{}", status=200),
            ],
        )

        # max_retries set as 4
        # backoff_factor set as 0 to avoid waiting while testing
        config = Config("token", None, 4, 0)
        try:
            DataSource.create(config, data={"test_date": date(2015, 1, 1)}).get()
        except RetryError:
            self.fail("request raised retryError unexpectedly!")
