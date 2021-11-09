import unittest

import requests_mock

from chartmogul import Account, Config, APIError


jsonResponse = {
  "name": u"Example Test Company",
  "currency": u"EUR",
  "time_zone": u"Europe/Berlin",
  "week_start_on": u"sunday"
}


class AccountTestCase(unittest.TestCase):
    """
    Tests account endpoint.
    """
    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/account",
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=200,
            json=jsonResponse
        )

        config = Config("token", "secret")  # is actually checked in mock
        account = Account.retrieve(config).get()
        self.assertTrue(isinstance(account, Account))
        self.assertEqual(account.name, "Example Test Company")
        self.assertEqual(account.currency, "EUR")
        self.assertEqual(account.time_zone, "Europe/Berlin")
        self.assertEqual(account.week_start_on, "sunday")
