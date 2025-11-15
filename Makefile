APP_BASE_IMAGE := web-app-base
APP_BASE_IMAGE_TAG := latest

ENV_FILE := .env
COMPOSE_FILE:= docker-compose.yaml
COMPOSE_FILE_PROXY:= docker-compose.traefik.yaml

.PHONY:
.ONESHELL:


# Building python virtual environment and installing dependencies
build-python-venv:
	python3 -m venv .venv
	source ./.venv/bin/activate
	pip3 install poetry
	poetry install --no-root


# Starting traefik-proxy service 
docker-up-proxy:
	docker network create proxy-public
	docker compose -f ${COMPOSE_FILE_PROXY} down
	docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE_PROXY} up -d --build --remove-orphans
	docker compose -f ${COMPOSE_FILE_PROXY} logs


# Stop traefik-proxy service
docker-down-proxy:
	docker compose -f ${COMPOSE_FILE_PROXY} down
	docker network rm proxy-public


# Build base backend image and run docker compose
# You may add "-d" flag to "docker compose up" command if you prefer detached launch
docker-build-run:
	docker build -t ${APP_BASE_IMAGE}:${APP_BASE_IMAGE_TAG} -f ./docker/Dockerfile.base .
	docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE} up --build


# Rerun docker compose with no building cache to ensure clean start
# You may add "-d" flag to "docker compose up" command if you prefer detached launch
docker-full-rerun:
	docker compose -f ${COMPOSE_FILE} down --rmi all
	docker system prune -af
	make docker-build-run


# Rerun docker compose
# You may add "-d" flag to "docker compose up" command if you prefer detached launch
docker-fast-rerun:
	docker compose -f ${COMPOSE_FILE} down app
	docker rmi main_app_image
	docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE} up --build
