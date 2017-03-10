import unittest
from datetime import datetime

import requests_mock

from chartmogul import Config
from chartmogul import Subscription


class SubscriptionsTestCase(unittest.TestCase):
    """
    Tests cancel, because it has custom path.
    """

    @requests_mock.mock()
    def test_cancel_subscription(self, mock_requests):
        """ Test cancel (patch) subscription (cancelled_at).
        """
        mock_requests.register_uri(
            'PATCH',
            "https://api.chartmogul.com/v1/import/subscriptions/some_uuid",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json={
                "uuid": "some_uuid",
                "external_id": "sub_0001",
                "customer_uuid": "cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
                "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                "cancellation_dates": ["2016-01-15T00:00:00.000Z"],
                "data_source_uuid": "ds_fef05d54-47b4-431b-aed2-eb6b9e545430"
            }
        )
        config = Config("token", "secret")  # is actually checked in mock
        result = Subscription.cancel(config,
                                     uuid="some_uuid",
                                     data={
                                         "cancelled_at": datetime(2016, 1, 15, 0, 0, 0)
                                     }).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), {
            "cancelled_at": "2016-01-15T00:00:00"})
        self.assertTrue(isinstance(result, Subscription))
        self.assertEqual(result.uuid, "some_uuid")

    @requests_mock.mock()
    def test_modify_subscription(self, mock_requests):
        """ Test modify (patch) subscription (cancellation_dates).
        """
        mock_requests.register_uri(
            'PATCH',
            "https://api.chartmogul.com/v1/import/subscriptions/some_uuid",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json={
                "uuid": "some_uuid",
                "external_id": "sub_0001",
                "customer_uuid": "cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
                "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                "cancellation_dates": [],
                "data_source_uuid": "ds_fef05d54-47b4-431b-aed2-eb6b9e545430"
            }
        )
        config = Config("token", "secret")  # is actually checked in mock
        result = Subscription.modify(config, uuid="some_uuid", data={
            "cancellation_dates": []}).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(),
                         {"cancellation_dates": []})
        self.assertEqual(str(result), str(Subscription(**{
            "uuid": u"some_uuid",
            "external_id": u"sub_0001",
            "customer_uuid": u"cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
            "plan_uuid": u"pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
            "cancellation_dates": [],
            "data_source_uuid": u"ds_fef05d54-47b4-431b-aed2-eb6b9e545430"
        })))
