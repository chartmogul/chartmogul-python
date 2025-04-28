import unittest
from chartmogul import Task, Config
import requests_mock

from pprint import pprint

task = {
    "uuid": "00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "assignee": "customer@example.com",
    "task_details": "This is some task details text.",
    "due_date": "2025-04-30T00:00:00Z",
    "completed_at": "2025-04-20T00:00:00Z",
    "created_at": "2025-04-01T12:00:00.000Z",
    "updated_at": "2025-04-01T12:00:00.000Z"
}

createTask = {
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "assignee": "customer@example.com",
    "task_details": "This is some task details text.",
    "due_date": "2025-04-30T00:00:00Z",
    "completed_at": "2025-04-20T00:00:00Z",
}

allTasks = {"entries": [task], "cursor": "cursor==", "has_more": False}


class TaskTestCase(unittest.TestCase):
    """
    Tests complex nested structure & assymetric create/retrieve schema.
    """

    @requests_mock.mock()
    def test_all(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/tasks?cursor=df431387&per_page=1&customer_uuid=cus_00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=allTasks,
        )

        config = Config("token")
        tasks = Task.all(
            config,
            customer_uuid="cus_00000000-0000-0000-0000-000000000000",
            cursor="df431387",
            per_page=1,
        ).get()
        expected = Task._many(**allTasks)

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "cursor": ["df431387"],
                "per_page": ["1"],
                "customer_uuid": ["cus_00000000-0000-0000-0000-000000000000"],
            },
        )
        self.assertEqual(mock_requests.last_request.text, None)
        self.assertEqual(dir(tasks), dir(expected))
        self.assertTrue(isinstance(tasks.entries[0], Task))
        self.assertFalse(tasks.has_more)
        self.assertEqual(tasks.cursor, "cursor==")

    @requests_mock.mock()
    def test_create(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/tasks", status_code=200, json=task
        )

        config = Config("token")
        expected = Task.create(config, data=createTask).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), createTask)
        self.assertTrue(expected, task)

    @requests_mock.mock()
    def test_patch(self, mock_requests):
        new_task = {
            "uuid": "00000000-0000-0000-0000-000000000000",
            "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
            "assignee": "customer@example.com",
            "task_details": "This is some task details text.",
            "due_date": "2025-04-30T00:00:00Z",
            "completed_at": "2025-04-20T00:00:00Z",
        }
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/tasks/00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=new_task,
        )

        new_task_details = {"task_details": "This is some other task details text."}

        config = Config("token")
        expected = Task.patch(
            config, uuid="00000000-0000-0000-0000-000000000000", data=new_task_details
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), new_task_details)
        self.assertTrue(isinstance(expected, Task))

    @requests_mock.mock()
    def test_retrieve(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/tasks/00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=task,
        )

        config = Config("token")
        expected = Task.retrieve(
            config, uuid="00000000-0000-0000-0000-000000000000"
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(isinstance(expected, Task))

    @requests_mock.mock()
    def test_destroy(self, mock_requests):
        mock_requests.register_uri(
            "DELETE",
            "https://api.chartmogul.com/v1/tasks/00000000-0000-0000-0000-000000000000",
            status_code=200,
            json={},
        )

        config = Config("token")
        expected = Task.destroy(
            config, uuid="00000000-0000-0000-0000-000000000000"
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertTrue(expected, {})
