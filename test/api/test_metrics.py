import unittest
import requests_mock
from chartmogul import Metrics, Config, APIError
from datetime import date
from collections import namedtuple
from chartmogul.api.metrics import Summary

allMetricsJSON = {
    "entries": [
        {
            "date": "2022-04-30",
            "mrr": 383859969,
            "mrr-percentage-change": 0.0,
            "arr": 4606319628,
            "arr-percentage-change": 0.0,
            "customer-churn-rate": 0.56,
            "customer-churn-rate-percentage-change": 0.0,
            "mrr-churn-rate": -0.17,
            "mrr-churn-rate-percentage-change": 0.0,
            "ltv": 117173214,
            "ltv-percentage-change": 0.0,
            "customers": 585,
            "customers-percentage-change": 0.0,
            "asp": 46107,
            "asp-percentage-change": 0.0,
            "arpa": 656170,
            "arpa-percentage-change": 0.0,
        },
        {
            "date": "2022-05-31",
            "mrr": 67028090,
            "mrr-percentage-change": 74.62,
            "arr": 8043370848,
            "arr-percentage-change": 74.62,
            "customer-churn-rate": 1.71,
            "customer-churn-rate-percentage-change": 205.36,
            "mrr-churn-rate": -74.52,
            "mrr-churn-rate-percentage-change": -43735.29,
            "ltv": 65112456,
            "ltv-percentage-change": -44.43,
            "customers": 602,
            "customers-percentage-change": 2.91,
            "asp": 22035,
            "asp-percentage-change": -52.21,
            "arpa": 1113423,
            "arpa-percentage-change": 69.69,
        },
    ],
    "summary": {
        "current-mrr": 670567114,
        "previous-mrr": 670012374,
        "mrr-percentage-change": 0.08,
        "current-arr": 8046805368,
        "previous-arr": 8040148488,
        "arr-percentage-change": 0.08,
        "current-customer-churn-rate": 1.71,
        "previous-customer-churn-rate": 0.56,
        "customer-churn-rate-percentage-change": 205.36,
        "current-mrr-churn-rate": -74.52,
        "previous-mrr-churn-rate": -0.17,
        "mrr-churn-rate-percentage-change": -43735.29,
        "current-ltv": 65112456,
        "previous-ltv": 117173214,
        "ltv-percentage-change": -44.43,
        "current-customers": 608,
        "previous-customers": 602,
        "customers-percentage-change": 1.0,
        "current-asp": 30397,
        "previous-asp": 18357,
        "asp-percentage-change": 65.59,
        "current-arpa": 1102906,
        "previous-arpa": 1112977,
        "arpa-percentage-change": -0.9,
    },
}

parsedEntries = [
    Metrics(
        **{
            "date": date(2022, 4, 30),
            "mrr": 383859969,
            "mrr_percentage_change": 0.0,
            "arr": 4606319628,
            "arr_percentage_change": 0.0,
            "customer_churn_rate": 0.56,
            "customer_churn_rate_percentage_change": 0.0,
            "mrr_churn_rate": -0.17,
            "mrr_churn_rate_percentage_change": 0.0,
            "ltv": 117173214.0,
            "ltv_percentage_change": 0.0,
            "customers": 585,
            "customers_percentage_change": 0.0,
            "asp": 46107.0,
            "asp_percentage_change": 0.0,
            "arpa": 656170.0,
            "arpa_percentage_change": 0.0,
        }
    ),
    Metrics(
        **{
            "date": date(2022, 5, 31),
            "mrr": 67028090,
            "mrr_percentage_change": 74.62,
            "arr": 8043370848,
            "arr_percentage_change": 74.62,
            "customer_churn_rate": 1.71,
            "customer_churn_rate_percentage_change": 205.36,
            "mrr_churn_rate": -74.52,
            "mrr_churn_rate_percentage_change": -43735.29,
            "ltv": 65112456.0,
            "ltv_percentage_change": -44.43,
            "customers": 602,
            "customers_percentage_change": 2.91,
            "asp": 22035.0,
            "asp_percentage_change": -52.21,
            "arpa": 1113423.0,
            "arpa_percentage_change": 69.69,
        }
    ),
]

mrrResponse = {
    "entries": [
        {
            "date": "2015-01-03",
            "mrr": 30000,
            "mrr-new-business": 10000,
            "mrr-expansion": 15000,
            "mrr-contraction": 0,
            "mrr-churn": 0,
            "mrr-reactivation": 0,
            "percentage-change": 0.0,
        },
        {
            "date": "2015-01-10",
            "mrr": 30000,
            "mrr-new-business": 0,
            "mrr-expansion": 0,
            "mrr-contraction": 0,
            "mrr-churn": 0,
            "mrr-reactivation": 0,
            "percentage-change": 74.62,
        },
    ],
    "summary": {"current": 43145000, "previous": 43145000, "percentage-change": 0.0},
}

parsedMrrEntries = [
    Metrics(
        **{
            "date": date(2015, 1, 3),
            "mrr": 30000,
            "mrr_new_business": 10000,
            "mrr_expansion": 15000,
            "mrr_contraction": 0,
            "mrr_churn": 0,
            "mrr_reactivation": 0,
            "percentage_change": 0.0,
        }
    ),
    Metrics(
        **{
            "date": date(2015, 1, 10),
            "mrr": 30000,
            "mrr_new_business": 0,
            "mrr_expansion": 0,
            "mrr_contraction": 0,
            "mrr_churn": 0,
            "mrr_reactivation": 0,
            "percentage_change": 74.62,
        }
    ),
]

ltvResponse = {
    "entries": [
        {"date": "2015-01-31", "ltv": 0, "percentage-change": 0.0},
        {"date": "2015-02-28", "ltv": 0, "percentage-change": -44.43},
        {"date": "2015-03-31", "ltv": 1862989.7959183701, "percentage-change": -44.43},
    ],
    "summary": {"current": 980568, "previous": 980568, "percentage-change": -44.43},
}

parsedLtvEntries = [
    Metrics(**{"date": date(2015, 1, 31), "ltv": 0.0, "percentage_change": 0.0}),
    Metrics(**{"date": date(2015, 2, 28), "ltv": 0.0, "percentage_change": -44.43}),
    Metrics(**{"date": date(2015, 3, 31), "ltv": 1862989.7959183701, "percentage_change": -44.43}),
]


class MetricsTestCase(unittest.TestCase):
    """
    Tests all & singular metrics - optional fields, optional namedtuple summary.
    """

    maxDiff = None

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            (
                "https://api.chartmogul.com/v1/metrics/all?start-date=2022-04-01"
                "&end-date=2022-05-31&interval=month&geo=GB&plans=PRO+Plan"
            ),
            status_code=200,
            json=allMetricsJSON,
        )

        config = Config("token")
        result = Metrics.all(
            config,
            start_date="2022-04-01",
            end_date="2022-05-31",
            interval="month",
            geo="GB",
            plans="PRO Plan",
        ).get()
        expected = Metrics._many(parsedEntries, summary=allMetricsJSON["summary"])

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "end-date": ["2022-05-31"],
                "geo": ["gb"],
                "interval": ["month"],
                "plans": ["pro plan"],
                "start-date": ["2022-04-01"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(result), str(expected))

    @requests_mock.mock()
    def test_mrr_summary(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            (
                "https://api.chartmogul.com/v1/metrics/mrr?start-date=2015-01-01"
                "&end-date=2015-11-01&interval=week"
            ),
            status_code=200,
            json=mrrResponse,
        )

        config = Config("token")
        result = Metrics.mrr(
            config, start_date="2015-01-01", end_date="2015-11-01", interval="week"
        ).get()
        expected = Metrics._many(parsedMrrEntries, summary=mrrResponse["summary"])
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {"end-date": ["2015-11-01"], "interval": ["week"], "start-date": ["2015-01-01"]},
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(result), str(expected))

    @requests_mock.mock()
    def test_ltv(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/metrics/ltv?start-date=2015-01-01&end-date=2015-11-01",
            status_code=200,
            json=ltvResponse,
        )

        config = Config("token")
        result = Metrics.ltv(config, start_date="2015-01-01", end_date="2015-11-01").get()
        expected = Metrics._many(parsedLtvEntries, summary=ltvResponse["summary"])
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {"end-date": ["2015-11-01"], "start-date": ["2015-01-01"]},
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(result), str(expected))
