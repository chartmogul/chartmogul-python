# pylama:ignore=W0212
import unittest

import requests_mock
from collections import namedtuple

from chartmogul import SubscriptionEvent
from chartmogul import Config
from chartmogul import APIError
from chartmogul import ArgumentMissingError

expected_sub_ev = {
     "id": 7654321,
     "external_id": "evnt_026",
     "customer_external_id": "scus_022",
     "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
     "event_type": "subscription_start_scheduled",
     "event_date": "2022-03-30",
     "effective_date": "2022-04-01",
     "subscription_external_id": "sub_0001",
     "plan_external_id": "gol d_monthly",
     "currency": "USD",
     "amount_in_cents": 1000
}

sub_ev_list_expected = {
    "subscription_events": [
    {
        "id": 7654321,
        "external_id": "evnt_026",
        "customer_external_id": "scus_022",
        "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
        "event_type": "subscription_start_scheduled",
        "event_date": "2022-03-30",
        "effective_date": "2022-04-01",
        "subscription_external_id": "sub_0001",
        "plan_external_id": "gol d_monthly",
        "currency": "USD",
        "amount_in_cents": 1000
    }
    ],
    "meta": {
        "next_key": 67048503,
        "prev_key": None,
        "before_key": "2022-04-10T22:27:35.834Z",
         "page": 1,
        "total_pages": 166
    }
}

sub_ev_one = SubscriptionEvent(
     id=7654321,
     external_id="evnt_026",
     customer_external_id="scus_022",
     data_source_uuid="ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
     event_type="subscription_start_scheduled",
     event_date="2022-03-30",
     effective_date="2022-04-01",
     subscription_external_id="sub_0001",
     plan_external_id="gol d_monthly",
     currency="USD",
     amount_in_cents=1000
)

class SubscriptionEventTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_create_subscription_event(self, mock_requests):
        sent = {
            "external_id": "evnt_026",
            "customer_external_id": "scus_022",
            "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
            "event_type": "subscription_start_scheduled",
            "event_date": "2022-03-30",
            "effective_date": "2022-04-01",
            "subscription_external_id": "sub_0001",
            "plan_external_id": "gold_monthly",
            "currency": "USD",
            "amount_in_cents": 1000
        }
        mock_requests.register_uri(
            'POST',
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=200,
            json=expected_sub_ev
        )
        config = Config("token")  # is actually checked in mock
        sub_ev = SubscriptionEvent.create(
            config,
            uuid = "UUID",
            data = sent
        ).get()
        expected = SubscriptionEvent(**expected_sub_ev)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), sent)
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))
        self.assertEqual(sub_ev.id,expected.id)
        self.assertEqual(sub_ev.external_id,expected.external_id)

    @requests_mock.mock()
    def test_delete_subscription_event_with_id(self, mock_requests):
        data = {"id": 7654321}
        mock_requests.register_uri(
            'DELETE',
            ("https://api.chartmogul.com/v1/subscription_events"),
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=204,
            json = data
        )

        config = Config("token")  # is actually checked in mock
        result = SubscriptionEvent.destroy_modify_with_params(config, data = data).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_delete_subscription_event_with_ds_uuid_and_external_id(self, mock_requests):
        data = {
            "data_source_uuid": "evnt_026",
            "external_id": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba"
        }
        mock_requests.register_uri(
            'DELETE',
            ("https://api.chartmogul.com/v1/subscription_events"),
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=204,
            json = data
        )

        config = Config("token")  # is actually checked in mock
        result = SubscriptionEvent.destroy_modify_with_params(config, data = data).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_modify_subscription_event_with_id(self, mock_requests):
        data={
            "id": 7654321,
            "amount_in_cents": 10
        }
        mock_requests.register_uri(
            'PATCH',
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=200,
            json=expected_sub_ev
        )
        config = Config("token")  # is actually checked in mock
        sub_ev = SubscriptionEvent.modify_with_params(config, data = data).get()

        expected = SubscriptionEvent(**expected_sub_ev)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), data)
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))
        self.assertEqual(sub_ev.id, 7654321)

    @requests_mock.mock()
    def test_modify_subscription_event_with_ds_uuid_and_external_id(self, mock_requests):
        data={
            "external_id": "evnt_026",
            "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
            "amount_in_cents": 10
        }
        mock_requests.register_uri(
            'PATCH',
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=200,
            json=expected_sub_ev
        )
        config = Config("token")  # is actually checked in mock
        sub_ev = SubscriptionEvent.modify_with_params(config, data=data).get()

        expected = SubscriptionEvent(**expected_sub_ev)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(),data)
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))
        self.assertEqual(sub_ev.id, 7654321)

    @requests_mock.mock()
    def test_modify_subscription_event_with_bad_params(self, mock_requests):
        data={
            "external_id": "evnt_026",
            "amount_in_cents": 10
        }
        mock_requests.register_uri(
            'PATCH',
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=200,
            json=expected_sub_ev
        )
        config = Config("token")  # is actually checked in mock
        try:
            sub_ev = SubscriptionEvent.modify_with_params(config, data=data).get()
        except ArgumentMissingError:
            pass
        else:
            self.fail('ArgumentMissingError not raised')

    @requests_mock.mock()
    def test_all_subscription_events(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=200,
            json=sub_ev_list_expected
        )

        config = Config("token")
        subscription_events = SubscriptionEvent.all(config).get()

        expected = SubscriptionEvent._many(
            subscription_events=[sub_ev_one],
            meta={
                "next_key": 67048503,
                "prev_key": None,
                "before_key": "2022-04-10T22:27:35.834Z",
                "page": 1,
                "total_pages": 166
           }
        )

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(sorted(dir(subscription_events)), sorted(dir(expected)))
        self.assertEqual(sorted(subscription_events.subscription_events[0].external_id), sorted(expected.subscription_events[0].external_id))
        self.assertTrue(isinstance(subscription_events.subscription_events[0], SubscriptionEvent))