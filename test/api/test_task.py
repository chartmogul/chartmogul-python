import unittest
from chartmogul import Task, Config
import requests_mock

from pprint import pprint

task = {
    "task_uuid": "00000000-0000-0000-0000-000000000000",
    "customer_uuid": "cus_00000000-0000-0000-0000-000000000000",
    "associated_object": "customer",
    "associated_object_uuid": "cus_00000000-0000-0000-0000-000000000000",
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

contactTask = {
    **task,
    "task_uuid": "00000000-0000-0000-0000-000000000001",
    "customer_uuid": None,
    "associated_object": "contact",
    "associated_object_uuid": "con_00000000-0000-0000-0000-000000000000",
}

createContactTask = {
    "associated_object_identifier": {
        "associated_object": "contact",
        "method": "uuid",
        "value": "con_00000000-0000-0000-0000-000000000000",
    },
    "assignee": "customer@example.com",
    "task_details": "This is some task details text.",
    "due_date": "2025-04-30T00:00:00Z",
}

allTasks = {"entries": [task], "cursor": "cursor==", "has_more": False}
allContactTasks = {"entries": [contactTask], "cursor": "cursor==", "has_more": False}


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
    def test_all_with_filters(self, mock_requests):
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/tasks?contact_uuid=con_00000000-0000-0000-0000-000000000000&assignee=customer@example.com&due_date_on_or_after=2025-04-01T00:00:00Z&due_date_on_or_before=2025-04-30T00:00:00Z&completed=false",
            status_code=200,
            json=allContactTasks,
        )

        config = Config("token")
        tasks = Task.all(
            config,
            contact_uuid="con_00000000-0000-0000-0000-000000000000",
            assignee="customer@example.com",
            due_date_on_or_after="2025-04-01T00:00:00Z",
            due_date_on_or_before="2025-04-30T00:00:00Z",
            completed=False,
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(
            mock_requests.last_request.qs,
            {
                "contact_uuid": ["con_00000000-0000-0000-0000-000000000000"],
                "assignee": ["customer@example.com"],
                "due_date_on_or_after": ["2025-04-01t00:00:00z"],
                "due_date_on_or_before": ["2025-04-30t00:00:00z"],
                "completed": ["false"],
            },
        )
        self.assertIsNone(tasks.entries[0].customer_uuid)
        self.assertEqual(tasks.entries[0].associated_object, "contact")
        self.assertEqual(
            tasks.entries[0].associated_object_uuid, "con_00000000-0000-0000-0000-000000000000"
        )

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
    def test_create_with_associated_object_identifier(self, mock_requests):
        mock_requests.register_uri(
            "POST", "https://api.chartmogul.com/v1/tasks", status_code=200, json=contactTask
        )

        config = Config("token")
        result = Task.create(config, data=createContactTask).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.json(), createContactTask)
        self.assertTrue(isinstance(result, Task))
        self.assertIsNone(result.customer_uuid)
        self.assertEqual(result.associated_object, "contact")

    @requests_mock.mock()
    def test_patch_not_modified(self, mock_requests):
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/tasks/00000000-0000-0000-0000-000000000000",
            status_code=304,
        )

        config = Config("token")
        result = Task.patch(
            config, uuid="00000000-0000-0000-0000-000000000000", data={}
        ).get()
        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(result, None)

    @requests_mock.mock()
    def test_patch(self, mock_requests):
        new_task = {
            "task_uuid": "00000000-0000-0000-0000-000000000000",
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
        self.assertEqual(expected.associated_object, "customer")

    @requests_mock.mock()
    def test_retrieve_without_associated_object(self, mock_requests):
        task_without_associated_object = {
            k: v for k, v in task.items()
            if k not in ("associated_object", "associated_object_uuid")
        }
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/tasks/00000000-0000-0000-0000-000000000000",
            status_code=200,
            json=task_without_associated_object,
        )

        config = Config("token")
        result = Task.retrieve(
            config, uuid="00000000-0000-0000-0000-000000000000"
        ).get()

        self.assertTrue(isinstance(result, Task))
        self.assertIsNone(result.associated_object)
        self.assertIsNone(result.associated_object_uuid)

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
