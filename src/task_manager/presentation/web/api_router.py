from fastapi import APIRouter

from .api import task_create, user_register


api_router = APIRouter(prefix="/api")


# USERS
_users_router = APIRouter(prefix="/users")

_users_router.add_api_route(
    "/register",
    user_register.route,
    name="api:register",
    methods=["POST"],
)

api_router.include_router(_users_router)


# TASKS
_tasks_router = APIRouter(prefix="/tasks")

_tasks_router.add_api_route(
    "/create",
    task_create.route,
    name="api:task_create",
    methods=["POST"],
)

api_router.include_router(_tasks_router)
