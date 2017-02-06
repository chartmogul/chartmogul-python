import unittest
import requests_mock
from chartmogul import Metrics, Config, APIError
from datetime import date
from collections import namedtuple
from chartmogul.api.metrics import Summary
allMetricsJSON = {
    "entries": [
        {
            "date": "2015-01-31",
            "customer-churn-rate": 20,
            "mrr-churn-rate": 14,
            "ltv": 1250.3,
            "customers": 331,
            "asp": 125,
            "arpa": 1250,
            "arr": 254000,
            "mrr": 21166
        },
        {
            "date": "2015-02-28",
            "customer-churn-rate": 20,
            "mrr-churn-rate": 22,
            "ltv": 1248,
            "customers": 329,
            "asp": 125,
            "arpa": 1250,
            "arr": 238000,
            "mrr": 21089
        }
    ]
}

parsedEntries = [
    Metrics(**{
            "date": date(2015, 1, 31),
            "customer_churn_rate": 20.0,
            "mrr_churn_rate": 14.0,
            "ltv": 1250.3,
            "customers": 331.0,
            "asp": 125.0,
            "arpa": 1250.0,
            "arr": 254000.0,
            "mrr": 21166.0
            }),
    Metrics(**{
            "date": date(2015, 2, 28),
            "customer_churn_rate": 20.0,
            "mrr_churn_rate": 22.0,
            "ltv": 1248.0,
            "customers": 329.0,
            "asp": 125.0,
            "arpa": 1250.0,
            "arr": 238000.0,
            "mrr": 21089.0
            })
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
            "mrr-reactivation": 0
        },
        {
            "date": "2015-01-10",
            "mrr": 30000,
            "mrr-new-business": 0,
            "mrr-expansion": 0,
            "mrr-contraction": 0,
            "mrr-churn": 0,
            "mrr-reactivation": 0
        }
    ],
    "summary": {
        "current": 43145000,
        "previous": 43145000,
        "percentage-change": 0.0
    }
}

parsedMrrEntries = [
    Metrics(**{
        "date": date(2015,1,3),
        "mrr": 30000.0,
        "mrr_new_business": 10000.0,
        "mrr_expansion": 15000.0,
        "mrr_contraction": 0.0,
        "mrr_churn": 0.0,
        "mrr_reactivation": 0.0
    }),
    Metrics(**{
        "date": date(2015,1,10),
        "mrr": 30000.0,
        "mrr_new_business": 0.0,
        "mrr_expansion": 0.0,
        "mrr_contraction": 0.0,
        "mrr_churn": 0.0,
        "mrr_reactivation": 0.0
    })
]


class MetricsTestCase(unittest.TestCase):
    """
    Tests all & singular metrics - optional fields, optional namedtuple summary.
    """

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            ("https://api.chartmogul.com/v1/metrics/all?start-date=2015-01-01"
             "&end-date=2015-11-24&interval=month&geo=GB&plans=PRO+Plan"),
            status_code=200,
            json=allMetricsJSON
        )

        config = Config("token", "secret")
        result = Metrics.all(config,
                             start_date='2015-01-01',
                             end_date='2015-11-24',
                             interval='month',
                             geo='GB',
                             plans='PRO Plan').get()
        expected = Metrics._many(parsedEntries)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {
            'end-date': ['2015-11-24'],
            'geo': ['gb'],
            'interval': ['month'],
            'plans': ['pro plan'],
            'start-date': ['2015-01-01']})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(result), str(expected))

    @requests_mock.mock()
    def test_mrr_summary(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            ("https://api.chartmogul.com/v1/metrics/mrr?start-date=2015-01-01"
             "&end-date=2015-11-01&interval=week"),
            status_code=200,
            json=mrrResponse
        )

        config = Config("token", "secret")
        result = Metrics.mrr(config,
                             start_date='2015-01-01',
                             end_date='2015-11-01',
                             interval='week').get()
        expected = Metrics._many(parsedMrrEntries, summary=mrrResponse["summary"])
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {
            'end-date': ['2015-11-01'],
            'interval': ['week'],
            'start-date': ['2015-01-01']})
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(str(result), str(expected))
