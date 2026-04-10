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


class SubscriptionEventDisablePathParamTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_disable_with_id_kwarg_uses_path_param(self, mock_requests):
        """disable(config, id=123) uses PATCH /subscription_events/{id}/disabled_state."""
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events/7654321/disabled_state",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        result = SubscriptionEvent.disable(config, id=7654321).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(
            mock_requests.last_request.json(), {"disabled": True}
        )
        self.assertTrue(isinstance(result, SubscriptionEvent))
        self.assertTrue(result.disabled)

    @requests_mock.mock()
    def test_enable_with_id_kwarg_uses_path_param(self, mock_requests):
        """enable(config, id=123) uses PATCH /subscription_events/{id}/disabled_state."""
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
        result = SubscriptionEvent.enable(config, id=7654321).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(
            mock_requests.last_request.json(), {"disabled": False}
        )
        self.assertFalse(result.disabled)
