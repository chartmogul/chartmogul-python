import unittest
from datetime import datetime

import requests_mock

from chartmogul import Config, Activity


class ActivitiesTestCase(unittest.TestCase):
    """
    Tests CustomerActivities
    """
    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/activities",
            request_headers={'Authorization': 'Basic dG9rZW46'},
            status_code=200,
            json={
                    "entries":[
                        {
                            "description": "purchased the plan_11 plan",
                            "activity-mrr-movement": 6000,
                            "activity-mrr": 6000,
                            "activity-arr": 72000,
                            "date": "2020-05-06T01:00:00",
                            "type": "new_biz",
                            "currency": "USD",
                            "subscription-external-id": "sub_2",
                            "plan-external-id": "11",
                            "customer-name": "customer_2",
                            "customer-uuid": "8bc55ab6-c3b5-11eb-ac45-2f9a49d75af7",
                            "customer-external-id": "customer_2",
                            "billing-connector-uuid": "99076cb8-97a1-11eb-8798-a73b507e7929",
                            "uuid": "f1a49735-21c7-4e3f-9ddc-67927aaadcf4"
                        },
                    ],
                    "has_more":False,
                    "per_page":200,
                }
        )
        config = Config("token")  # is actually checked in mock
        result = Activity.all(config).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result.__class__.__name__, Activity._many.__name__)
        self.assertEqual(result.entries[0].uuid, 'f1a49735-21c7-4e3f-9ddc-67927aaadcf4')
