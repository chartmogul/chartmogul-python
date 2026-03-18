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
    "event_date": "2022-03-30 23:00:00.000",
    "effective_date": "2022-04-01 23:00:00.000",
    "subscription_external_id": "sub_0001",
    "plan_external_id": "gol d_monthly",
    "currency": "USD",
    "amount_in_cents": 1000,
    "event_order": 123,
}

sub_ev_list_expected = {
    "subscription_events": [
        {
            "id": 7654321,
            "external_id": "evnt_026",
            "customer_external_id": "scus_022",
            "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
            "event_type": "subscription_start_scheduled",
            "event_date": "2022-03-30 23:00:00.000",
            "effective_date": "2022-04-01 23:00:00.000",
            "subscription_external_id": "sub_0001",
            "plan_external_id": "gol d_monthly",
            "currency": "USD",
            "amount_in_cents": 1000,
            "event_order": 123,
        }
    ],
    "cursor": "cursor==",
    "has_more": False,
}

sub_ev_one = SubscriptionEvent(
    id=7654321,
    external_id="evnt_026",
    customer_external_id="scus_022",
    data_source_uuid="ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
    event_type="subscription_start_scheduled",
    event_date="2022-03-30 23:00:00.000",
    effective_date="2022-04-01 23:00:00.000",
    subscription_external_id="sub_0001",
    plan_external_id="gol d_monthly",
    currency="USD",
    amount_in_cents=1000,
)


class SubscriptionEventTestCase(unittest.TestCase):
    @requests_mock.mock()
    def test_create_subscription_event(self, mock_requests):
        sent = {
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
        }
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )
        config = Config("token")  # is actually checked in mock
        sub_ev = SubscriptionEvent.create(config, uuid="UUID", data=sent).get()
        expected = SubscriptionEvent(**expected_sub_ev)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), sent)
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))
        self.assertEqual(sub_ev.id, expected.id)
        self.assertEqual(sub_ev.external_id, expected.external_id)

    @requests_mock.mock()
    def test_delete_subscription_event_with_id(self, mock_requests):
        data = {"subscription_event": {"id": 7654321}}
        mock_requests.register_uri(
            "DELETE",
            ("https://api.chartmogul.com/v1/subscription_events"),
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
            json=data,
        )

        config = Config("token")  # is actually checked in mock
        result = SubscriptionEvent.destroy_with_params(config, data=data).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_delete_subscription_event_with_ds_uuid_and_external_id(self, mock_requests):
        data = {
            "subscription_event": {
                "data_source_uuid": "evnt_026",
                "external_id": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
            }
        }
        mock_requests.register_uri(
            "DELETE",
            ("https://api.chartmogul.com/v1/subscription_events"),
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
            json=data,
        )

        config = Config("token")  # is actually checked in mock
        result = SubscriptionEvent.destroy_with_params(config, data=data).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_modify_subscription_event_with_id(self, mock_requests):
        data = {"subscription_event": {"id": 7654321, "amount_in_cents": 10}}
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )
        config = Config("token")  # is actually checked in mock
        sub_ev = SubscriptionEvent.modify_with_params(config, data=data).get()

        expected = SubscriptionEvent(**expected_sub_ev)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), data)
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))
        self.assertEqual(sub_ev.id, 7654321)

    @requests_mock.mock()
    def test_modify_subscription_event_with_ds_uuid_and_external_id(self, mock_requests):
        data = {
            "subscription_event": {
                "external_id": "evnt_026",
                "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
                "amount_in_cents": 10,
            }
        }
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )
        config = Config("token")  # is actually checked in mock
        sub_ev = SubscriptionEvent.modify_with_params(config, data=data).get()

        expected = SubscriptionEvent(**expected_sub_ev)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), data)
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))
        self.assertEqual(sub_ev.id, 7654321)

    @requests_mock.mock()
    def test_modify_subscription_event_with_bad_params(self, mock_requests):
        data = {"subscription_event": {"external_id": "evnt_026", "amount_in_cents": 10}}
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=400,
            json=expected_sub_ev,
        )
        config = Config("token")  # is actually checked in mock
        try:
            sub_ev = SubscriptionEvent.modify_with_params(config, data=data).get()
        except ArgumentMissingError:
            pass
        else:
            self.fail("ArgumentMissingError not raised")

    @requests_mock.mock()
    def test_all_subscription_events(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=sub_ev_list_expected,
        )

        config = Config("token")
        subscription_events = SubscriptionEvent.all(config).get()

        expected = SubscriptionEvent._many(
            subscription_events=[sub_ev_one], has_more=True, cursor="cursor=="
        )

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(sorted(dir(subscription_events)), sorted(dir(expected)))
        self.assertEqual(
            sorted(subscription_events.subscription_events[0].external_id),
            sorted(expected.subscription_events[0].external_id),
        )
        self.assertTrue(isinstance(subscription_events.subscription_events[0], SubscriptionEvent))

    @requests_mock.mock()
    def test_destroy_flat_params(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
        )

        config = Config("token")
        result = SubscriptionEvent.destroy(config, data={"id": 7654321}).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.json(),
            {"subscription_event": {"id": 7654321}},
        )
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_modify_flat_params(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        sub_ev = SubscriptionEvent.modify(
            config, data={"id": 7654321, "amount_in_cents": 10}
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.json(),
            {"subscription_event": {"id": 7654321, "amount_in_cents": 10}},
        )
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))
        self.assertEqual(sub_ev.id, 7654321)

    @requests_mock.mock()
    def test_disable_subscription_event(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        sub_ev = SubscriptionEvent.disable(config, data={"id": 7654321}).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        body = mock_requests.last_request.json()
        self.assertEqual(body["subscription_event"]["id"], 7654321)
        self.assertTrue(body["subscription_event"]["disabled"])
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))

    @requests_mock.mock()
    def test_enable_subscription_event(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        sub_ev = SubscriptionEvent.enable(config, data={"id": 7654321}).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        body = mock_requests.last_request.json()
        self.assertEqual(body["subscription_event"]["id"], 7654321)
        self.assertFalse(body["subscription_event"]["disabled"])

    @requests_mock.mock()
    def test_destroy_flat_with_external_id_and_ds_uuid(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
        )

        config = Config("token")
        result = SubscriptionEvent.destroy(
            config,
            data={
                "external_id": "evnt_026",
                "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
            }
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.json(),
            {
                "subscription_event": {
                    "external_id": "evnt_026",
                    "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
                }
            },
        )
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_modify_flat_with_external_id_and_ds_uuid(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        sub_ev = SubscriptionEvent.modify(
            config,
            data={
                "external_id": "evnt_026",
                "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
                "amount_in_cents": 10,
            }
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.json(),
            {
                "subscription_event": {
                    "external_id": "evnt_026",
                    "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
                    "amount_in_cents": 10,
                }
            },
        )
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))

    @requests_mock.mock()
    def test_destroy_flat_passthrough_envelope(self, mock_requests):
        """If caller already wraps in subscription_event, don't double-wrap."""
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=204,
        )

        config = Config("token")
        result = SubscriptionEvent.destroy(
            config,
            data={"subscription_event": {"id": 7654321}}
        ).get()

        self.assertEqual(
            mock_requests.last_request.json(),
            {"subscription_event": {"id": 7654321}},
        )
        self.assertTrue(result is None)

    @requests_mock.mock()
    def test_modify_flat_passthrough_envelope(self, mock_requests):
        """If caller already wraps in subscription_event, don't double-wrap."""
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        sub_ev = SubscriptionEvent.modify(
            config,
            data={"subscription_event": {"id": 7654321, "amount_in_cents": 10}}
        ).get()

        self.assertEqual(
            mock_requests.last_request.json(),
            {"subscription_event": {"id": 7654321, "amount_in_cents": 10}},
        )
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))

    @requests_mock.mock()
    def test_disable_with_external_id_and_ds_uuid(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        sub_ev = SubscriptionEvent.disable(
            config,
            data={
                "external_id": "evnt_026",
                "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
            }
        ).get()

        body = mock_requests.last_request.json()
        self.assertEqual(body["subscription_event"]["external_id"], "evnt_026")
        self.assertEqual(
            body["subscription_event"]["data_source_uuid"],
            "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
        )
        self.assertTrue(body["subscription_event"]["disabled"])
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))

    @requests_mock.mock()
    def test_enable_with_external_id_and_ds_uuid(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        config = Config("token")
        sub_ev = SubscriptionEvent.enable(
            config,
            data={
                "external_id": "evnt_026",
                "data_source_uuid": "ds_1fm3eaac-62d0-31ec-clf4-4bf0mbe81aba",
            }
        ).get()

        body = mock_requests.last_request.json()
        self.assertEqual(body["subscription_event"]["external_id"], "evnt_026")
        self.assertFalse(body["subscription_event"]["disabled"])
        self.assertTrue(isinstance(sub_ev, SubscriptionEvent))

    @requests_mock.mock()
    def test_all_subscription_events_with_filters(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/subscription_events?external_id=evnt_026"
            "&customer_external_id=scus_022&event_type=subscription_start_scheduled&plan_external_id=gol d_monthly",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=sub_ev_list_expected,
        )

        config = Config("token")
        subscription_events = SubscriptionEvent.all(
            config,
            external_id="evnt_026",
            customer_external_id="scus_022",
            event_type="subscription_start_scheduled",
            plan_external_id="gol d_monthly",
        ).get()

        expected = SubscriptionEvent._many(
            [SubscriptionEvent(**expected_sub_ev)], has_more=True, cursor="cursor=="
        )

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "customer_external_id": ["scus_022"],
                "event_type": ["subscription_start_scheduled"],
                "external_id": ["evnt_026"],
                "plan_external_id": ["gol d_monthly"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(sorted(dir(subscription_events)), sorted(dir(expected)))
        self.assertEqual(
            sorted(subscription_events.subscription_events[0].external_id),
            sorted(expected.subscription_events[0].external_id),
        )
        self.assertTrue(isinstance(subscription_events.subscription_events[0], SubscriptionEvent))

    @requests_mock.mock()
    def test_disable_passthrough_envelope_sets_flag_inside(self, mock_requests):
        """When caller passes pre-wrapped envelope, disabled flag must go inside it."""
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        caller_data = {"subscription_event": {"id": 7654321}}
        config = Config("token")
        SubscriptionEvent.disable(config, data=caller_data).get()

        body = mock_requests.last_request.json()
        # disabled must be inside the envelope, not at top level
        self.assertNotIn("disabled", body)
        self.assertTrue(body["subscription_event"]["disabled"])
        self.assertEqual(body["subscription_event"]["id"], 7654321)
        # caller's dict must not be mutated
        self.assertNotIn("disabled", caller_data["subscription_event"])

    @requests_mock.mock()
    def test_enable_passthrough_envelope_sets_flag_inside(self, mock_requests):
        """When caller passes pre-wrapped envelope, disabled=False must go inside it."""
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        caller_data = {"subscription_event": {"id": 7654321}}
        config = Config("token")
        SubscriptionEvent.enable(config, data=caller_data).get()

        body = mock_requests.last_request.json()
        self.assertNotIn("disabled", body)
        self.assertFalse(body["subscription_event"]["disabled"])
        self.assertEqual(body["subscription_event"]["id"], 7654321)
        self.assertNotIn("disabled", caller_data["subscription_event"])

    @requests_mock.mock()
    def test_disable_does_not_mutate_caller_dict(self, mock_requests):
        """Flat-param disable must not mutate the caller's dict in-place."""
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/subscription_events",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_sub_ev,
        )

        caller_data = {"id": 7654321}
        config = Config("token")
        SubscriptionEvent.disable(config, data=caller_data).get()

        # caller's original dict should not have been modified
        self.assertNotIn("disabled", caller_data)
