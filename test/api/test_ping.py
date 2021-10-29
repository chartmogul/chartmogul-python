import unittest

import requests_mock

from chartmogul import Ping, Config, APIError


class PingTestCase(unittest.TestCase):
    """
    Tests authorization is passed correctly and ping GET alias.
    """

    @requests_mock.mock()
    def test_ping(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/ping",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json={"data": "pong!"}
        )

        config = Config("token")  # is actually checked in mock
        pong = Ping.ping(config).get()
        expected = Ping(**{"data": u"pong!"})
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(pong), str(expected))
