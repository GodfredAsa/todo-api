from model.task_model import TaskModel
from tests.integration.integration_base_test import IntegrationBaseTest


class TestTaskModel(IntegrationBaseTest):

    def test_create_task(self):
        with self.app_context():
            task = TaskModel(name="Test Task", description="This is a test task.", user_id="456", status="pending", priority="medium")
           
            task.save_to_db()
            self.assertIsNotNone(TaskModel.find_by_uuid(task.task_id), "Task is saved")
            self.assertEqual(TaskModel.find_by_uuid(task.task_id).name, task.name, "Task is saved")

    def test_find_task_by_uuid(self):
            with self.app_context():
                task = TaskModel(name="Test Task", description="This is a test task.", user_id="456", status="pending", priority="medium")
                task.save_to_db()
                self.assertEqual(TaskModel.find_by_uuid(task.task_id), TaskModel.find_by_user_id(task.user_id)[0], "Task is saved")

    def test_find_task_by_user_id(self):
        with self.app_context():
            task = TaskModel(name="Test Task", description="This is a test task.", user_id="456", status="pending", priority="medium")
            task.save_to_db()
            self.assertEqual(TaskModel.find_by_user_id(task.user_id)[0], task, "Task is saved")

    def test_find_task_by_user_id_and_task_id(self):
        with self.app_context():
            task = TaskModel(name="Test Task", description="This is a test task.", user_id="456", status="pending", priority="medium")
            task.save_to_db()
            self.assertEqual(TaskModel.find_task_by_user_id_and_task_id(task.user_id, task.task_id), task, "Task is saved")

    def test_find_task_by_user_id_and_task_id_not_found(self):
        with self.app_context():
            task = TaskModel(name="Test Task", description="This is a test task.", user_id="456", status="pending", priority="medium")
            task.save_to_db()
            self.assertIsNone(TaskModel.find_task_by_user_id_and_task_id("123", task.task_id), "Task is not found")
            self.assertIsNone(TaskModel.find_task_by_user_id_and_task_id(task.user_id, "123"), "Task is not found")

    
