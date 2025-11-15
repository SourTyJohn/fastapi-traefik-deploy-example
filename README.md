# FastAPI + Traefik + Nginx + Postgres 

- [x] FastAPI backend implementing "Clean Architecture"
- [x] PostgreSQL database for persistent storage
- [x] Nginx static files server
- [x] Traefik proxy
- [ ] Redis based api token verification
- [ ] Traefik letsencrypt SSL for HTTPS
- [ ] Frontend
- [ ] GitHub Actions CI/CD

src directory stores backend

docker directory stores Dockerfiles and entrypoints

## .env File

```
CERTRESOLVER=letsencrypt


# DOMAIN
DOMAIN_EMAIL=  # for letsencrypt certresolver if you use real domain
DOMAIN_URL=localhost


# BACKEND
BACKEND_SECRET_KEY=chagethis
BACKEND_DEBUG=True
BACKEND_ALLOWED_HOSTS=localhost, 127.0.0.1
BACKEND_CSRF_TRUSTED_ORIGINS=http://localhost, http://127.0.0.1
BACKEND_DB_ECHO=0  # sqlalchemy db_echo
BACKEND_DB_NAME=backend


# DATABASE
POSTGRES_PASSWORD=chagethis
POSTGRES_USER=chagethis
POSTGRES_DB=default


# NETWORK
NETWORK_BACKEND_URL=/api
NETWORK_BACKEND_HOST=app
NETWORK_BACKEND_PORT=8000

NETWORK_DATABASE_HOST=postgres-db
NETWORK_DATABASE_PORT=5432

NETWORK_NGINX_HOST=nginx
NETWORK_NGINX_PORT=6060
NETWORK_NGINX_STATIC_URL=/static/

NETWORK_TRAEFIK_HOST=app
NETWORK_TRAEFIK_PORT=80  # you may replace it with other, if system does not allow 80
NETWORK_TRAEFIK_DASHBOARD_PORT=9000


#
MAKE_MIGRATIONS_DB_URI=postgresql+psycopg://chagethis
```

## Build Python Venv for Development

```
make build-python-venv
```

I am using Ruff (charliermarsh.ruff) extension for code formating


## Local deploy with http using compose

Majority of required operations implemented in [Makefile](Makefile) for convenience.
You may read it, to look under the hood of all operations.

#### First run

Firstly, you need to create network and start traefik proxy service using:

```
make docker-up-proxy
```

> If Traefik service gives you Permission Denied error for docker.sock you can either:
> 1) add current user to docker group and relogin
> 2) launch command with sudo (admin privileges)
>
> All docker related commands should be executed from single user

And after it, you ready to up other services.

```
make docker-build-run
```

#### Rerun with soft rebuild of web-app service

```
make docker-fast-rerun
```

#### Rerun from scratch

```
make docker-full-rerun
```


## Running

http://localhost/api/docs for FastAPI swagger view

http://localhost:9000 for traefik dashboard
