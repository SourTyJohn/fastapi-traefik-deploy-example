APP_BASE_IMAGE := web-app-base
APP_BASE_IMAGE_TAG := latest

ENV_FILE := .env
COMPOSE_FILE:= docker-compose.yaml
COMPOSE_FILE_PROXY:= docker-compose.traefik.yaml

.PHONY:
.ONESHELL:


build-python-venv:
	python3 -m venv .venv
	source ./.venv/bin/activate
	pip3 install poetry
	poetry install --no-root


docker-up-proxy:
	docker network create proxy-public
	docker compose -f ${COMPOSE_FILE_PROXY} down
	docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE_PROXY} up -d --build --remove-orphans
	docker compose -f ${COMPOSE_FILE_PROXY} logs


docker-down-proxy:
	docker compose -f ${COMPOSE_FILE_PROXY} down
	docker network rm proxy-public


docker-build-run:
	docker build -t ${APP_BASE_IMAGE}:${APP_BASE_IMAGE_TAG} -f ./docker/Dockerfile.base .
	docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE} up -d --build
	docker compose -f ${COMPOSE_FILE} logs


docker-full-rerun:
	docker compose -f ${COMPOSE_FILE} down
	docker compose -f ${COMPOSE_FILE} rm -f
	docker rmi $$(docker compose -f ${COMPOSE_FILE} images -q) -f
	make docker-build-run
	docker compose -f ${COMPOSE_FILE} logs


docker-fast-rerun:
	docker compose -f ${COMPOSE_FILE} down app
	docker rmi main_app_image
	docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE} up --build
	docker compose -f ${COMPOSE_FILE} logs
