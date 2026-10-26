from unittest.mock import patch

from flask_jwt_extended import create_access_token

from db import db
from enums.task_priority import TaskPriority
from enums.task_status import TaskStatus
from model.task_model import TaskModel
from model.user_model import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest


class TestTaskSearchResource(IntegrationBaseTest):
    def setUp(self):
        super().setUp()
        with self.app_context():
            self.user = UserModel(
                preferred_name="Task Search User",
                password="hashed-password",
            )
            db.session.add(self.user)
            db.session.commit()
            self.user_id = self.user.user_id
            self.access_token = create_access_token(identity=self.user_id)
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
            }

            tasks = [
                TaskModel(
                    user_id=self.user_id,
                    name="Complete API assignment",
                    description="",
                    priority=TaskPriority.HIGH,
                    status=TaskStatus.PENDING,
                ),
                TaskModel(
                    user_id=self.user_id,
                    name="Buy groceries",
                    description="",
                    priority=TaskPriority.LOW,
                    status=TaskStatus.COMPLETED,
                ),
            ]
            db.session.add_all(tasks)
            db.session.commit()

    def test_search_tasks_by_user_status_name_and_priority(self):
        response = self.app.get(
            "/api/v1/tasks/search",
            query_string={
                "user_id": self.user_id,
                "status": "pending",
                "name": "api",
                "priority": "high",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        tasks = response.get_json()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["name"], "Complete API assignment")

    def test_search_tasks_requires_user_id(self):
        response = self.app.get(
            "/api/v1/tasks/search",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "user_id is required")

    def test_search_tasks_rejects_invalid_status(self):
        response = self.app.get(
            "/api/v1/tasks/search",
            query_string={"user_id": self.user_id, "status": "unknown"},
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid status", response.get_json()["message"])

    def test_search_tasks_rejects_invalid_priority(self):
        response = self.app.get(
            "/api/v1/tasks/search",
            query_string={"user_id": self.user_id, "priority": "immediate"},
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid priority", response.get_json()["message"])

    def test_search_tasks_returns_not_found_for_unknown_user(self):
        response = self.app.get(
            "/api/v1/tasks/search",
            query_string={"user_id": "unknown-user"},
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["message"], "User not found")

    def test_search_tasks_returns_custom_internal_server_error(self):
        with patch(
            "resource.task_resource.TaskModel.find_tasks_by_filters",
            side_effect=RuntimeError("database failure"),
        ):
            response = self.app.get(
                "/api/v1/tasks/search",
                query_string={"user_id": self.user_id},
                headers=self.headers,
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.get_json(),
            {
                "status": 500,
                "message": "Internal Server Error",
                "data": None,
            },
        )
