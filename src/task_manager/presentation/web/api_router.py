from fastapi import APIRouter

from .users import me, register

from .realms import create, list_owned


api_router = APIRouter()


# USERS
_users_router = APIRouter(prefix="/users", tags=["users"])

_users_router.add_api_route(
    "/register",
    register.route,
    name="api:register",
    methods=["POST"],
)

_users_router.add_api_route(
    "/me",
    me.route,
    name="api:user_me",
    methods=["GET"],
)

api_router.include_router(_users_router)


# TASKS
_realms_router = APIRouter(prefix="/realms", tags=["realms"])

_realms_router.add_api_route(
    "/create",
    create.route,
    name="api:realm_create",
    methods=["POST"],
)

_realms_router.add_api_route(
    "/own",
    list_owned.route,
    name="api:realm_own_list",
    methods=["GET"],
)

api_router.include_router(_realms_router)
