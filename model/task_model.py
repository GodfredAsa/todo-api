from datetime import datetime, timezone
from db import db
from enums.task_priority import TaskPriority
from enums.task_status import TaskStatus
from model.user_model import UserModel
from typing import List, Optional
from utils.utils import format_created_date, generate_uuid


class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(20))
    user_id = db.Column(db.String(100), db.ForeignKey("users.id"))
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    priority = db.Column(
        db.Enum(
            TaskPriority,
            values_callable=lambda enum_cls: [e.value for e in enum_cls]
        ),
        nullable=False,
        default=TaskPriority.MEDIUM
    )

    status = db.Column(
        db.Enum(
            TaskStatus,
            values_callable=lambda enum_cls: [e.value for e in enum_cls]
        ),
        nullable=False,
        default=TaskStatus.PENDING
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    def __init__(
        self, user_id, name, description,
        priority, status
    ):
        self.user_id = user_id
        self.task_id = generate_uuid()
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = datetime.now(timezone.utc)

    def __str__(self):
        return (
            f"<TaskID: ID:{self.task_id}, "
            f"name:{self.name}, "
            f"priority:{self.priority}, "
            f"status:{self.status}, "
            f"description:{self.description}, "
            f"created_at:{self.created_at}>"
        )

    def to_json(self):
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": format_created_date(),
            "user": UserModel.find_by_uuid(self.user_id).to_dict() if self.user_id else None
        }


    @classmethod
    def find_by_uuid(cls, task_id: str) -> 'TaskModel':
        return cls.query.filter_by(task_id=task_id).first()

    @classmethod
    def find_tasks_by_user_id(cls, user_id: str) -> List['TaskModel']:
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_tasks_by_filters(
        cls,
        user_id: str,
        status: Optional[TaskStatus] = None,
        name: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List['TaskModel']:
        query = cls.query.filter_by(user_id=user_id)
        if status is not None:
            query = query.filter_by(status=status)
        if priority is not None:
            query = query.filter_by(priority=priority)
        if name:
            query = query.filter(cls.name.ilike(f"%{name}%"))
        return query.all()

    @classmethod
    def find_task_by_user_id_and_task_id(cls, user_id: str, task_id: str) -> 'TaskModel':
        return cls.query.filter_by(user_id=user_id, task_id=task_id).first()

    @classmethod
    def find_by_user_id(cls, user_id: str) -> List['TaskModel']:
        return cls.query.filter_by(user_id=user_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
