from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi

from task_manager.presentation.web import api_router
from task_manager.ioc import make_app_ioc
from task_manager.config import Config, load_env_config


def create_app() -> FastAPI:
    config = load_env_config()
    di_container = make_app_ioc(context={Config: config})

    app = FastAPI(
        debug=True,
        openapi_url=f"{config.web.NETWORK_BACKEND_URL}/openapi.jsom",
        docs_url=f"{config.web.NETWORK_BACKEND_URL}/docs",
    )
    app.include_router(api_router)
    setup_dishka_fastapi(di_container, app)
    return app


app = create_app()
