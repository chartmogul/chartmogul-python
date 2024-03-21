import unittest
from chartmogul import Opportunity, Config
import requests_mock

opportunity = {
    "uuid": "00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "owner": "test1@example.org",
    "pipeline": "New business 1",
    "pipeline_stage": "Discovery",
    "estimated_close_date": "2023-12-22",
    "currency": "USD",
    "amount_in_cents": 100,
    "type": "recurring",
    "forecast_category": "pipeline",
    "win_likelihood": 3,
    "custom": {"from_campaign": True},
    "created_at": "2024-03-13T07:33:28.356Z",
    "updated_at": "2024-03-13T07:33:28.356Z"
}

createOpportunity = {
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "owner": "test1@example.org",
    "pipeline": "New business 1",
    "pipeline_stage": "Discovery",
    "estimated_close_date": "2023-12-22",
    "currency": "USD",
    "amount_in_cents": 100,
    "type": "recurring",
    "forecast_category": "pipeline",
    "win_likelihood": 3,
    "custom": {"key": "from_campaign", "value": True},
}


allOpportunities = {"entries": [opportunity], "cursor": "cursor==", "has_more": True}


class OpportunityTestCase(unittest.TestCase):
    """
    Tests complex nested structure & assymetric create/retrieve schema.
    """

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/opportunities?cursor=ym9vewfo&per_page=1&customer_uuid=cus_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=allOpportunities,
        )

        config = Config("token")
        opportunities = Opportunity.all(
            config,
            customer_uuid="cus_00000000-0000-0000-0000-000000000000",
            cursor="ym9vewfo",
            per_page=1,
        ).get()
        expected = Opportunity._many(**allOpportunities)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "cursor": ["ym9vewfo"],
                "per_page": ["1"],
                "customer_uuid": ["cus_00000000-0000-0000-0000-000000000000"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(dir(opportunities), dir(expected))
        self.assertTrue(isinstance(opportunities.entries[0], Opportunity))
        self.assertTrue(opportunities.has_more)
        self.assertEqual(opportunities.cursor, "cursor==")

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/opportunities", status_code=200, json=opportunity
        )

        config = Config("token")
        expected = Opportunity.create(config, data=createOpportunity).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createOpportunity)
        self.assertTrue(expected, opportunity)

    @requests_mock.mock()
    def test_patch(self, mock_requests):
        opportunity = {
            "uuid": "00000000-0000-0000-0000-000000000000",
            "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
            "owner": "test1@example.org",
            "pipeline": "New business 1",
            "pipeline_stage": "Discovery",
            "estimated_close_date": "2023-12-22",
            "currency": "USD",
            "amount_in_cents": 100,
            "type": "recurring",
            "forecast_category": "pipeline",
            "win_likelihood": 3,
            "custom": {"from_campaign": True},
        }
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/opportunities/00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=opportunity,
        )

        new_estimated_close_date = {"estimated_close_date": "2024-12-22"}

        config = Config("token")
        expected = Opportunity.patch(
            config, uuid="00000000-0000-0000-0000-000000000000", data=new_estimated_close_date
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), new_estimated_close_date)
        self.assertTrue(isinstance(expected, Opportunity))

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/opportunities/00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=opportunity,
        )

        config = Config("token")
        expected = Opportunity.retrieve(
            config, uuid="00000000-0000-0000-0000-000000000000"
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(expected, Opportunity))

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/opportunities/00000000-0000-0000-0000-000000000000",
            status_code=200,
            json={},
        )

        config = Config("token")
        expected = Opportunity.destroy(
            config, uuid="00000000-0000-0000-0000-000000000000"
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(expected, {})
