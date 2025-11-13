FROM web-app-base:latest

    WORKDIR /app

    COPY --chmod=755 src/ ./src/
    COPY --chmod=755 ./docker/backend/entrypoint.sh ./src/entrypoint.sh


WORKDIR ./src/

ENTRYPOINT [ "sh", "./entrypoint.sh" ]
