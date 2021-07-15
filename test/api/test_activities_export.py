import unittest
from datetime import datetime

import requests_mock

from chartmogul import Config
from chartmogul import ActivitiesExport


class ActivitiesExportTestCase(unittest.TestCase):
    """
    Tests Creating ActivitiesExport request
    """
    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            'POST',
            "https://api.chartmogul.com/v1/activities_export",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json={
                    "id": "618b6698-c6d0-42e9-8c4f-6a2bda5ac472",
                    "status": "pending",
                    "file_url": None,
                    "params": {
                        "kind": "activities",
                        "params": {}
                    },
                    "expires_at": None,
                    "created_at": "2021-07-15T08:23:40+00:00"
                }
        )
        config = Config("token", "secret")  # is actually checked in mock
        result = ActivitiesExport.create(config, data={})

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result.get().id, '618b6698-c6d0-42e9-8c4f-6a2bda5ac472')

    """
    Tests Retrieving ActivitiesExport status
    """
    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            'GET',
            "https://api.chartmogul.com/v1/activities_export/618b6698-c6d0-42e9-8c4f-6a2bda5ac472",
            request_headers={'Authorization': 'Basic dG9rZW46c2VjcmV0'},
            status_code=200,
            json={
                    "id": "618b6798-c6d0-42e0-8c4f-6a2bdb5ac412",
                    "status": "succeeded",
                    "file_url": "https://customer-export.s3.eu-east-1.amazonaws.com/activities-a-2e135794-207e-4623-a485-87fa0a0cc9c5.zip",
                    "params": {
                        "kind": "activities",
                        "params": {}
                    },
                    "expires_at": "2021-07-22T08:23:41+00:00",
                    "created_at": "2021-07-15T08:23:40+00:00"
                }
        )
        config = Config("token", "secret")  # is actually checked in mock
        result = ActivitiesExport.retrieve(config, id='618b6698-c6d0-42e9-8c4f-6a2bda5ac472')

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {'id': ['618b6698-c6d0-42e9-8c4f-6a2bda5ac472']})
        self.assertEqual(result.get().status, 'succeeded')
