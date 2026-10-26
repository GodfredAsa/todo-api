from flask_restful import reqparse
from constant.user_constant import BLANK_ERROR
from enums.task_priority import TaskPriority
from enums.task_status import TaskStatus

_task_parser = reqparse.RequestParser()

_task_parser.add_argument(
    "name",
    type=str,
    required=True,
    help=BLANK_ERROR.format("name"),
)

_task_parser.add_argument(
    "description",
    type=str,
    required=False,
    default=None,
    help=BLANK_ERROR.format("description"),
)

_task_parser.add_argument(
    "priority",
    type=str,
    choices=[priority.value for priority in TaskPriority],
    required=False,
    default=TaskPriority.MEDIUM.value,
    help="Priority must be LOW, MEDIUM, HIGH, or URGENT.",
)

_task_parser.add_argument(
    "status",
    type=str,
    choices=[status.value for status in TaskStatus],
    required=False,
    default=TaskStatus.PENDING.value,
    help="Status must be PENDING, IN_PROGRESS, COMPLETED, or CANCELLED.",
)


def get_task_data():
    return _task_parser.parse_args()
