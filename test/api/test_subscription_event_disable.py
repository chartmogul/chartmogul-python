import unittest

import requests_mock

from chartmogul import SubscriptionEvent, Config


expected_sub_ev = {
    "id": 7654321,
    "external_id": "evnt_026",
    "customer_external_id": "scus_022",
    "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
    "event_type": "subscription_start_scheduled",
    "event_date": "2022-03-30 23:00:00.000",
    "effective_date": "2022-04-01 23:00:00.000",
    "subscription_external_id": "sub_0001",
    "plan_external_id": "gold_monthly",
    "currency": "USD",
    "amount_in_cents": 1000,
    "disabled": True,
}


class SubscriptionEventDisableByIdTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_disable_by_id(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events/7654321/disabled_state",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        result = SubscriptionEvent.disable_by_id(
            config, id=7654321, data={"disabled": True}
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(
            mock_requests.last_request.json(), {"disabled": True}
        )
        self.assertTrue(isinstance(result, SubscriptionEvent))
        self.assertTrue(result.disabled)

    @requests_mock.mock()
    def test_enable_by_id(self, mock_requests):
        enabled = dict(expected_sub_ev)
        enabled["disabled"] = False

        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events/7654321/disabled_state",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=enabled,
        )

        config = Config("token")
        result = SubscriptionEvent.disable_by_id(
            config, id=7654321, data={"disabled": False}
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertFalse(result.disabled)
