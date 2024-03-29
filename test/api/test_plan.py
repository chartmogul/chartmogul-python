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
        expected_plan_dict = {
            "uuid": "whatever_uuid",
            "data_source_uuid": "some_uuid",
            "name": "some plan",
            "interval_count": 2,
            "interval_unit": "moonshines",
            "external_id": "custom_filter",
        }
        mock_requests.register_uri(
            "GET",
            (
                "https://api.chartmogul.com/v1/plans?"
                "&per_page=12&data_source_uuid=some_uuid&external_id=custom_filter"
            ),
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json={
                "plans": [expected_plan_dict],
                "cursor": "cursor==",
                "has_more": False,
            },
        )
        config = Config("token")  # is actually checked in mock
        plan = Plan.all(
            config,
            per_page=12,
            data_source_uuid="some_uuid",
            external_id="custom_filter",
        ).get()
        expected = Plan._many([Plan(**expected_plan_dict)], cursor="cursor==", has_more=False)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "data_source_uuid": ["some_uuid"],
                "external_id": ["custom_filter"],
                "per_page": ["12"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(plan), str(expected))

    @requests_mock.mock()
    def test_modify_plan(self, mock_requests):
        expected_plan_dict = {
            "uuid": "whatever_uuid",
            "data_source_uuid": "some_uuid",
            "name": "new_name",
            "interval_count": 2,
            "interval_unit": "moonshines",
            "external_id": "custom_filter",
        }
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/plans/whatever_uuid",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_plan_dict,
        )
        config = Config("token")  # is actually checked in mock
        plan = Plan.modify(config, uuid="whatever_uuid", data={"name": "new_name"}).get()
        expected = Plan(**expected_plan_dict)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), {"name": "new_name"})
        self.assertEqual(str(plan), str(expected))

    @requests_mock.mock()
    def test_create_plan(self, mock_requests):
        expected_plan_dict = {
            "uuid": "whatever_uuid",
            "data_source_uuid": "some_uuid",
            "name": "new_name",
            "interval_count": 2,
            "interval_unit": "moonshines",
            "external_id": "custom_filter",
        }
        sent = {
            "data_source_uuid": "ds_9bb53a1e-edfd-11e6-bf83-af49e978cb11",
            "name": "Gold Plan",
            "interval_count": 1,
            "interval_unit": "month",
            "external_id": "plan_0002",
        }
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/plans",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_plan_dict,
        )
        config = Config("token")  # is actually checked in mock
        plan = Plan.create(config, data=sent).get()
        expected = Plan(**expected_plan_dict)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), sent)
        self.assertEqual(str(plan), str(expected))
