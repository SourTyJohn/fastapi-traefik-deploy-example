from fastapi.security import APIKeyHeader
from fastapi import FastAPI, Depends

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi

from task_manager.presentation.web import api_router
from task_manager.bootstrap.di import make_app_ioc
from task_manager.bootstrap.config import Config, load_env_config


def create_app() -> FastAPI:
    config = load_env_config()
    di_container = make_app_ioc(context={Config: config})

    app = FastAPI(
        debug=True,
        root_path=f"{config.web.NETWORK_BACKEND_URL}",
        # openapi_url=f"{config.web.NETWORK_BACKEND_URL}/openapi.json",
        # docs_url=f"{config.web.NETWORK_BACKEND_URL}/docs",
        dependencies=[
            # for displaing "Authorize" button
            Depends(
                APIKeyHeader(
                    name=config.auth.TOKEN_HEADER_NAME,
                    auto_error=False,
                )
            )
        ],
        #
    )
    app.include_router(api_router)
    setup_dishka_fastapi(di_container, app)
    return app


app = create_app()
