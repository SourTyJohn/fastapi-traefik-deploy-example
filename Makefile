.ONESHELL:


APP_BASE_IMAGE := web-app-base
APP_BASE_IMAGE_TAG := latest
COMPOSE_ENV_FILE := .env
COMPOSE_ENV_FILE_DEV := .env


docker-actions-build:
# this step is used in github actions workflow
	docker build -t ${APP_BASE_IMAGE}:${APP_BASE_IMAGE_TAG} -f ./docker/Dockerfile.base .
	docker compose --env-file ${COMPOSE_ENV_FILE} build


docker-build-run:
	sudo docker build -t ${APP_BASE_IMAGE}:${APP_BASE_IMAGE_TAG} -f ./docker/Dockerfile.base .
	sudo docker compose --env-file ${COMPOSE_ENV_FILE} up -d 


docker-full-rerun:
	sudo docker compose down
	sudo docker system prune -af
	sudo make docker-build-run


docker-fast-rerun:
	sudo docker compose down app
	sudo docker rmi main_app_image
	sudo docker compose --env-file ${COMPOSE_ENV_FILE} up -d


docker-dev-build-run:
	sudo docker build -t ${APP_BASE_IMAGE}:${APP_BASE_IMAGE_TAG} -f ./docker/Dockerfile.base .
	sudo docker compose --env-file ${COMPOSE_ENV_FILE_DEV} -f docker-compose-dev.yaml up -d 


docker-dev-full-rerun:
	sudo docker compose down
	sudo docker compose down -f docker-compose-dev.yaml
	sudo docker system prune -af
	sudo make docker-dev-build-run


docker-dev-fast-rerun:
	sudo docker compose down app
	sudo docker rmi main_app_image
	sudo docker compose --env-file ${COMPOSE_ENV_FILE_DEV} -f docker-compose-dev.yaml up -d


makemigrations:
	cd polski_news
	python3 manage.py makemigrations


migrate:
	cd polski_news
	python3 manage.py migrate
