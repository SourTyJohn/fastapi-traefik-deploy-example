from dishka import (
    AsyncContainer,
    make_async_container,
)

from dishka.integrations.fastapi import FastapiProvider

from task_manager.ioc.providers import (
    DbProvider,
    GatewaysProvider,
    ApiInteractorsProvider,
    CommonsProvider,
    MiddlewaresProvider,
)


def make_app_ioc(context: dict = {}) -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        DbProvider(),
        GatewaysProvider(),
        CommonsProvider(),
        ApiInteractorsProvider(),
        MiddlewaresProvider(),
        context=context,
    )
