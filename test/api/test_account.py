import unittest

import requests_mock

from chartmogul import Account, Config, APIError


jsonResponse = {
    "name": "Example Test Company",
    "currency": "EUR",
    "time_zone": "Europe/Berlin",
    "week_start_on": "sunday",
}


class AccountTestCase(unittest.TestCase):
    """
    Tests account endpoint.
    """

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/account",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=jsonResponse,
        )

        config = Config("token")  # is actually checked in mock
        account = Account.retrieve(config).get()
        self.assertTrue(isinstance(account, Account))
        self.assertEqual(account.name, "Example Test Company")
        self.assertEqual(account.currency, "EUR")
        self.assertEqual(account.time_zone, "Europe/Berlin")
        self.assertEqual(account.week_start_on, "sunday")


jsonResponseWithId = {
    "id": "acct_a1b2c3d4",
    "name": "Example Test Company",
    "currency": "EUR",
    "time_zone": "Europe/Berlin",
    "week_start_on": "sunday",
}


class AccountIdTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_retrieve_with_id(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/account",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=jsonResponseWithId,
        )

        config = Config("token")
        account = Account.retrieve(config).get()
        self.assertTrue(isinstance(account, Account))
        self.assertEqual(account.id, "acct_a1b2c3d4")

    @requests_mock.mock()
    def test_retrieve_without_id_field(self, mock_requests):
        """Old API responses without id field should not break deserialization."""
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/account",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=jsonResponse,
        )

        config = Config("token")
        account = Account.retrieve(config).get()
        self.assertTrue(isinstance(account, Account))
        self.assertFalse(hasattr(account, "id"))


jsonResponseWithInclude = {
    "name": "Example Test Company",
    "currency": "EUR",
    "time_zone": "Europe/Berlin",
    "week_start_on": "sunday",
    "churn_recognition": "immediate",
    "churn_when_zero_mrr": "ignore",
}


class AccountIncludeTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_retrieve_with_include(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/account?include=churn_recognition,churn_when_zero_mrr",
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            json=jsonResponseWithInclude,
        )

        config = Config("token")
        account = Account.retrieve(
            config, include="churn_recognition,churn_when_zero_mrr"
        ).get()
        self.assertTrue(isinstance(account, Account))
        self.assertEqual(account.churn_recognition, "immediate")
        self.assertEqual(account.churn_when_zero_mrr, "ignore")
        self.assertEqual(
            mock_requests.last_request.qs,
            {"include": ["churn_recognition,churn_when_zero_mrr"]},
        )

    @requests_mock.mock()
    def test_retrieve_with_single_include(self, mock_requests):
        singleIncludeResponse = {
            "name": "Example Test Company",
            "currency": "EUR",
            "time_zone": "Europe/Berlin",
            "week_start_on": "sunday",
            "churn_recognition": "immediate",
        }

        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/account?include=churn_recognition",
            request_headers={"Authorization": "Basic dG9rZW46"},
            headers={"Content-Type": "application/json"},
            status_code=200,
            json=singleIncludeResponse,
        )

        config = Config("token")
        account = Account.retrieve(config, include="churn_recognition").get()
        self.assertTrue(isinstance(account, Account))
        self.assertEqual(account.churn_recognition, "immediate")
        self.assertFalse(hasattr(account, "churn_when_zero_mrr"))
