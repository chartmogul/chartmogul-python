import unittest

from chartmogul import PlanGroup, Config, APIError
import requests_mock
from collections import namedtuple


class PlanGroupTestCase(unittest.TestCase):
    """
    Tests plan_groups endpoints.
    """

    @requests_mock.mock()
    def test_create_plan_group(self, mock_requests):
        expected_plan_group_dict = {
            "uuid": "whatever_uuid",
            "name": "Gold Plan Group",
            "plans_count": 2,
        }
        sent = {
            "name": "Gold Plan Group",
            "plans": [
                "pl_fe0824c8-4738-11ea-a26c-3b021eb4c733",
                "pl_fe160a70-4738-11ea-a26c-e38e12dbd8be",
            ],
        }
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/plan_groups",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_plan_group_dict,
        )
        config = Config("token")  # is actually checked in mock
        plan_group = PlanGroup.create(config, data=sent).get()
        expected = PlanGroup(**expected_plan_group_dict)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), sent)
        self.assertEqual(str(plan_group), str(expected))

    @requests_mock.mock()
    def test_retrieve_plan_group(self, mock_requests):
        expected_plan_group_dict = {
            "uuid": "whatever_uuid",
            "name": "Gold Plan Group",
            "plans_count": 2,
        }
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/plan_groups/whatever_uuid",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_plan_group_dict,
        )

        config = Config("token")  # is actually checked in mock
        result = PlanGroup.retrieve(config, uuid="whatever_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(result, PlanGroup))
        self.assertEqual(result.uuid, "whatever_uuid")
        self.assertEqual(result.name, "Gold Plan Group")
        self.assertEqual(result.plans_count, 2)

    @requests_mock.mock()
    def test_retrieve_plan_group_plans_old_pagination(self, mock_requests):
        expected_plans = {
            "plans": [
                {
                    "name": "Berghain Flatrate Pack - bi-annual",
                    "uuid": "pl_cef31082-37be-11ea-a7bc-cb55fa0afcbb",
                    "data_source_uuid": "ds_73c24b7e-37be-11ea-85a4-03a4322daccc",
                    "interval_count": 6,
                    "interval_unit": "month",
                    "external_id": "plan_EOwj9vInDKILy1",
                },
                {
                    "name": "Berghain Flatrate Pack - Skip the Queue Pack",
                    "uuid": "pl_cef46630-37be-11ea-a7bc-a316cc9407e9",
                    "data_source_uuid": "ds_73c24b7e-37be-11ea-85a4-03a4322daccc",
                    "interval_count": 1,
                    "interval_unit": "month",
                    "external_id": "plan_EOsEG3pyySMBEP",
                },
            ],
            "current_page": 1,
            "total_pages": 1,
        }
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/plan_groups/whatever_uuid/plans",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_plans,
        )

        config = Config("token")  # is actually checked in mock
        result = PlanGroup.all(config, uuid="whatever_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result.plans[0].uuid, "pl_cef31082-37be-11ea-a7bc-cb55fa0afcbb")
        self.assertEqual(result.plans[1].uuid, "pl_cef46630-37be-11ea-a7bc-a316cc9407e9")
        self.assertEqual(len(result.plans), 2)
        self.assertEqual(result.total_pages, 1)
        self.assertEqual(result.current_page, 1)

    @requests_mock.mock()
    def test_retrieve_plan_group_plans_new_pagination(self, mock_requests):
        expected_plans = {
            "plans": [
                {
                    "name": "Berghain Flatrate Pack - bi-annual",
                    "uuid": "pl_cef31082-37be-11ea-a7bc-cb55fa0afcbb",
                    "data_source_uuid": "ds_73c24b7e-37be-11ea-85a4-03a4322daccc",
                    "interval_count": 6,
                    "interval_unit": "month",
                    "external_id": "plan_EOwj9vInDKILy1",
                },
                {
                    "name": "Berghain Flatrate Pack - Skip the Queue Pack",
                    "uuid": "pl_cef46630-37be-11ea-a7bc-a316cc9407e9",
                    "data_source_uuid": "ds_73c24b7e-37be-11ea-85a4-03a4322daccc",
                    "interval_count": 1,
                    "interval_unit": "month",
                    "external_id": "plan_EOsEG3pyySMBEP",
                },
            ],
            "has_more": False,
            "cursor": "cursor==",
        }
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/plan_groups/whatever_uuid/plans",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_plans,
        )

        config = Config("token")  # is actually checked in mock
        result = PlanGroup.all(config, uuid="whatever_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result.plans[0].uuid, "pl_cef31082-37be-11ea-a7bc-cb55fa0afcbb")
        self.assertEqual(result.plans[1].uuid, "pl_cef46630-37be-11ea-a7bc-a316cc9407e9")
        self.assertEqual(len(result.plans), 2)
        self.assertEqual(result.cursor, "cursor==")
        self.assertFalse(result.has_more)

    @requests_mock.mock()
    def test_all_plan_groups_old_pagination(self, mock_requests):
        expected_plan_groups = {
            "plan_groups": [
                {"uuid": "whatever_uuid", "name": "good_plan", "plans_count": 2},
                {"uuid": "my_uuid", "name": "best_plan", "plans_count": 5},
            ],
            "current_page": 1,
            "total_pages": 1,
        }
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/plan_groups",
            status_code=200,
            json=expected_plan_groups,
        )

        config = Config("token")
        result = PlanGroup.all(config).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertTrue(isinstance(result.plan_groups[0], PlanGroup))
        self.assertEqual(result.plan_groups[0].uuid, "whatever_uuid")
        self.assertEqual(result.plan_groups[1].uuid, "my_uuid")
        self.assertEqual(result.total_pages, 1)
        self.assertEqual(result.current_page, 1)

    @requests_mock.mock()
    def test_all_plan_groups_new_pagination(self, mock_requests):
        expected_plan_groups = {
            "plan_groups": [
                {"uuid": "whatever_uuid", "name": "good_plan", "plans_count": 2},
                {"uuid": "my_uuid", "name": "best_plan", "plans_count": 5},
            ],
            "has_more": False,
            "cursor": "cursor==",
        }
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/plan_groups",
            status_code=200,
            json=expected_plan_groups,
        )

        config = Config("token")
        result = PlanGroup.all(config).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertTrue(isinstance(result.plan_groups[0], PlanGroup))
        self.assertEqual(result.plan_groups[0].uuid, "whatever_uuid")
        self.assertEqual(result.plan_groups[1].uuid, "my_uuid")
        self.assertFalse(result.has_more)
        self.assertEqual(result.cursor, "cursor==")

    @requests_mock.mock()
    def test_destroy_plan_group(self, mock_requests):
        mock_requests.register_uri(
            "DELETE", "https://api.chartmogul.com/v1/plan_groups/my_uuid", status_code=204
        )

        config = Config("token")
        result = PlanGroup.destroy(config, uuid="my_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(result, None)

    @requests_mock.mock()
    def test_modify_plan_group_name(self, mock_requests):
        expected_plan_group_dict = {"uuid": "whatever_uuid", "name": "new_name", "plans_count": 2}
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/plan_groups/whatever_uuid",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_plan_group_dict,
        )
        config = Config("token")  # is actually checked in mock
        result = PlanGroup.modify(config, uuid="whatever_uuid", data={"name": "new_name"}).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), {"name": "new_name"})
        self.assertEqual(result.uuid, "whatever_uuid")
        self.assertEqual(result.name, "new_name")
        self.assertEqual(result.plans_count, 2)

    @requests_mock.mock()
    def test_modify_plan_group_plans(self, mock_requests):
        expected_plan_group_dict = {"uuid": "whatever_uuid", "name": "new_name", "plans_count": 3}
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/plan_groups/whatever_uuid",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_plan_group_dict,
        )
        config = Config("token")  # is actually checked in mock
        result = PlanGroup.modify(
            config, uuid="whatever_uuid", data={"plans": "[pl_uuid_1, pl_uuid_2, pl_uuid_3]"}
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result.plans_count, 3)
