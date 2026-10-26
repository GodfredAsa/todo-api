
from model.task_model import TaskModel
from tests.unit.unit_base_test import UnitBaseTest
import json

class TestTaskModel(UnitBaseTest):

    def test_task_construction(self):
        task = TaskModel(name="Test Task", description="This is a test task.", user_id="user123", priority="MEDIUM", status="PENDING")
    
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.description, "This is a test task.")
        self.assertEqual(task.user_id, "user123")
        self.assertEqual(task.priority, "MEDIUM")
        self.assertEqual(task.status, "PENDING")
        self.assertIsNone(task.id)