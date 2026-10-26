
from http import HTTPStatus

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from enums.task_priority import TaskPriority
from enums.task_status import TaskStatus
from exceptions import BadRequestException, NotFoundException
from model.task_model import TaskModel
from model.user_model import UserModel
from utils.api_response import CustomApiResponse


class TaskResource(Resource):

    @jwt_required()
    def post(self):
        data = request.get_json(silent=True) or {}

        user_id = data.get("user_id")
        name = data.get("name")
        priority = data.get("priority", TaskPriority.MEDIUM.value)
        status = data.get("status", TaskStatus.PENDING.value)

        if not user_id:
            raise BadRequestException("user_id is required")
        if not name:
            raise BadRequestException("name is required")

        valid_priorities = [item.value for item in TaskPriority]

        if priority not in valid_priorities:
            raise BadRequestException(
                f"Invalid priority. Allowed values: {valid_priorities}"
            )

        valid_statuses = [item.value for item in TaskStatus]

        if status not in valid_statuses:
            raise BadRequestException(
                f"Invalid status. Allowed values: {valid_statuses}"
            )

        if not UserModel.exists_by_user_id(user_id):
            raise NotFoundException("User not found")

        data["priority"] = TaskPriority(priority)
        data["status"] = TaskStatus(status)
        data.setdefault("description", None)
        task = TaskModel(**data)
        task.save_to_db()
        return CustomApiResponse.get_response(
            HTTPStatus.CREATED,
            "Task created successfully",
            task.to_json(),
        ), HTTPStatus.CREATED


class TasksByUserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        if not UserModel.find_by_uuid(user_id):
            raise NotFoundException("User not found")
        return [task.to_json() for task in TaskModel.find_tasks_by_user_id(user_id)]


class TaskSearchResource(Resource):
    @jwt_required()
    def get(self):
        user_id = request.args.get("user_id")
        status = request.args.get("status")
        name = request.args.get("name")
        priority = request.args.get("priority")

        if not user_id:
            raise BadRequestException("user_id is required")
        if not UserModel.find_by_uuid(user_id):
            raise NotFoundException("User not found")

        valid_statuses = [item.value for item in TaskStatus]
        if status and status not in valid_statuses:
            raise BadRequestException(
                f"Invalid status. Allowed values: {valid_statuses}"
            )

        valid_priorities = [item.value for item in TaskPriority]
        if priority and priority not in valid_priorities:
            raise BadRequestException(
                f"Invalid priority. Allowed values: {valid_priorities}"
            )

        tasks = TaskModel.find_tasks_by_filters(
            user_id=user_id,
            status=TaskStatus(status) if status else None,
            name=name,
            priority=TaskPriority(priority) if priority else None,
        )
        return [task.to_json() for task in tasks]



class TaskByUserResource(Resource):
    @jwt_required()
    def get(self, user_id, task_id):
        user_task = TaskModel.find_task_by_user_id_and_task_id(user_id, task_id)
        if not user_task:
            raise NotFoundException("User with Task not not found")

        return CustomApiResponse.get_response(
                HTTPStatus.OK,
                "User task successfully retrieved",
                user_task.to_json(),
            ), HTTPStatus.OK

    @jwt_required()
    def delete(self, user_id, task_id):
        user_task = TaskModel.find_task_by_user_id_and_task_id(user_id, task_id)
        if not user_task:
            raise NotFoundException("User with Task not not found")

        user_task.delete_from_db()
        return CustomApiResponse.get_response(
            HTTPStatus.OK,
            "User task deleted successfully",
            None,
        ), HTTPStatus.OK

    @jwt_required()
    def put(self, user_id, task_id):
        data = request.get_json(silent=True) or {}
        user_task = TaskModel.find_task_by_user_id_and_task_id(user_id, task_id)
        if not user_task:
            raise NotFoundException("User with Task not not found")

        priority = data.get("priority")
        status = data.get("status")
        if not data.get("name"):
            raise BadRequestException("name is required")

        valid_priorities = [item.value for item in TaskPriority]
        valid_statuses = [item.value for item in TaskStatus]

        if priority not in valid_priorities:
            raise BadRequestException(
                f"Invalid priority. Allowed values: {valid_priorities}"
            )

        if status not in valid_statuses:
            raise BadRequestException(
                f"Invalid status. Allowed values: {valid_statuses}"
            )

        user_task.task_id = task_id
        user_task.user_id = user_id
        user_task.name = data["name"]
        user_task.priority = data["priority"]
        user_task.status = data["status"]
        user_task.description = data.get("description")

        user_task.save_to_db()

        return CustomApiResponse.get_response(
            HTTPStatus.OK,
            "User task updated successfully",
            user_task.to_json(),
        ), HTTPStatus.OK