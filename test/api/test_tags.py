import unittest

from chartmogul import Tags, Config, APIError
import requests_mock
from collections import namedtuple


class TagsTestCase(unittest.TestCase):
    """
    Tests tags can be added.
    """

    @requests_mock.mock()
    def test_add(self, mock_requests):
        requestData = {"tags": ["important", "Prio1"]}
        expected_dict = {"tags": ["engage", "unit loss", "discountable", "important", "Prio1"]}
        mock_requests.register_uri(
            "POST",
            "https://api.chartmogul.com/v1/customers/UUID/attributes/tags",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json=expected_dict,
        )
        config = Config("token")  # is actually checked in mock
        tags = Tags.add(config, uuid="UUID", data=requestData).get()
        expected = Tags(**expected_dict)
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), requestData)
        self.assertEqual(str(tags), str(expected))
