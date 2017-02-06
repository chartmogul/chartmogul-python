import unittest
import requests_mock
from chartmogul import Metrics, Config, APIError
from datetime import date
from collections import namedtuple

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
            "date": date(2015,2,28),
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


class MetricsTestCase(unittest.TestCase):
    """
    Tests all & singular metrics - optional fields, optional namedtuple summary.
    """

    @requests_mock.mock()
    def test_create(self, mock_requests):
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
