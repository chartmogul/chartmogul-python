import unittest

from chartmogul import Plan, Config, APIError
import requests_mock
from collections import namedtuple


class PlanTestCase(unittest.TestCase):
    """
    Tests cursor query parameters & modify (patch a plan).
    """

    @requests_mock.mock()
    def test_cursor_list_plans(self, mock_requests):
        expected_plan_dict = {"uuid": u"whatever_uuid",
                              "data_source_uuid": u"some_uuid",
                              "name": u"some plan",
                              "interval_count": 2,
                              "interval_unit": u"moonshines",
                              "external_id": u"custom_filter"}
        mock_requests.register_uri(
            'GET',
            ("https://api.chartmogul.com/v1/plans?page=5"
            "&per_page=12&data_source_uuid=some_uuid&external_id=custom_filter"),
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json={"plans": [expected_plan_dict],
                  "current_page": 5,
                  "total_pages": 18}
        )
        config = Config("token", "secret")  # is actually checked in mock
        plan = Plan.all(config, page=5, per_page=12,
                        data_source_uuid="some_uuid",
                        external_id="custom_filter").get()
        expected = Plan._many([Plan(**expected_plan_dict)],
                              current_page=5, total_pages=18)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {
            'data_source_uuid': ['some_uuid'],
            'external_id': ['custom_filter'],
            'page': ['5'],
            'per_page': ['12']
        })
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(plan), str(expected))

    @requests_mock.mock()
    def test_modify_plan(self, mock_requests):
        expected_plan_dict = {
            "uuid": u"whatever_uuid",
            "data_source_uuid": u"some_uuid",
            "name": u"new_name",
            "interval_count": 2,
            "interval_unit": u"moonshines",
            "external_id": u"custom_filter"
        }
        mock_requests.register_uri(
            'PATCH',
            "https://api.chartmogul.com/v1/plans/whatever_uuid",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json=expected_plan_dict
        )
        config = Config("token", "secret")  # is actually checked in mock
        plan = Plan.modify(config,
                           uuid="whatever_uuid",
                           data={"name": "new_name"}).get()
        expected = Plan(**expected_plan_dict)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(),
                         {"name": u"new_name"})
        self.assertEqual(str(plan), str(expected))
