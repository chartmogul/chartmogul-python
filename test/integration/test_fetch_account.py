import unittest
import requests_mock
from chartmogul import Config, Account

config = Config(api_key="-")


class FetchAccountTestCase(unittest.TestCase):
    """
    Tests fetching account details.
    """

    @requests_mock.Mocker()
    def test_fetch_account(self, m):
        m.get(
            "https://api.chartmogul.com/v1/account",
            json={
                "name": "Chartmogul Test",
                "currency": "EUR",
                "time_zone": "Europe/Lisbon",
                "week_start_on": "monday",
            },
            status_code=200,
        )

        account = Account.retrieve(config).get()
        self.assertTrue(isinstance(account, Account))
        self.assertEqual(account.name, "Chartmogul Test")
        self.assertEqual(account.currency, "EUR")
        self.assertEqual(account.time_zone, "Europe/Lisbon")
        self.assertEqual(account.week_start_on, "monday")
