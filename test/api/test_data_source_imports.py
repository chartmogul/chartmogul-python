import unittest

import requests_mock

from chartmogul import DataSource, Config


class DataSourceImportsTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_import_json(self, mock_requests):
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/data_sources/ds_123/json_imports",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json={"id": "imp_456"},
        )

        config = Config("token")
        result = DataSource.import_json(
            config, uuid="ds_123", data={"customers": []}
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertEqual(
            mock_requests.last_request.json(), {"customers": []}
        )

    @requests_mock.mock()
    def test_import_status(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/data_sources/ds_123/json_imports/imp_456",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json={
                "uuid": "ds_123",
                "name": "test",
                "created_at": "2025-01-01T00:00:00.000Z",
                "status": "idle",
                "system": "Import API",
            },
        )

        config = Config("token")
        result = DataSource.import_status(
            config, uuid="ds_123", import_id="imp_456"
        ).get()

        self.assertEqual(mock_requests.call_count, 1)
        self.assertTrue(isinstance(result, DataSource))
