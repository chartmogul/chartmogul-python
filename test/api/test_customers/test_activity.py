import unittest
from datetime import datetime

import requests_mock

from chartmogul import Config, CustomerActivity


class CustomerActivitiesTestCase(unittest.TestCase):
    """
    Tests CustomerActivities
    """
    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/customers/some_uuid/activities",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json={
                    "entries":[
                        {
                            "activity-arr": 24000,
                            "activity-mrr": 2000,
                            "activity-mrr-movement": 2000,
                            "currency": "USD",
                            "currency-sign": "$",
                            "date": "2015-06-09T13:16:00-04:00",
                            "description": "purchased the Silver Monthly plan (1)",
                            "id": 48730,
                            "type": "new_biz",
                            "subscription-external-id": "1"
                        }
                    ],
                    "has_more":False,
                    "per_page":200,
                    "page":1
                }
        )
        config = Config("token")  # is actually checked in mock
        result = CustomerActivity.all(config, uuid="some_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result.__class__.__name__, CustomerActivity._many.__name__)
        self.assertEqual(result.entries[0].id, 48730)
