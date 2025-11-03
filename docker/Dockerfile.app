FROM web-app-base:latest

    WORKDIR /app

    # -- App Directory --
    COPY --chmod=755 polski_news/ ./polski_news/
    COPY --chmod=755 entrypoint.sh ./polski_news/entrypoint.sh
    # -- --

    COPY --chmod=755 templates/ ./templates/
    COPY --chmod=755 static/ ./static/


# -- App Directory --
WORKDIR ./polski_news/
# -- --

ENTRYPOINT [ "sh", "./entrypoint.sh" ]
