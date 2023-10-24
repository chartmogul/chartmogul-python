import unittest
import vcr
from chartmogul import Config, Account

config = Config(api_key="-")


class FetchAccountTestCase(unittest.TestCase):
    """
    Tests errors & user mistakes.
    """

    @vcr.use_cassette("fixtures/fetch_account.yaml", filter_headers=["authorization"], record=True)
    def test_fetch_account(self):
        account = Account.retrieve(config).get()
        self.assertTrue(isinstance(account, Account))
