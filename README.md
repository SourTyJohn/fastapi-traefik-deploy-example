# Ja Pierdole


## .env file

```
SECRET_KEY=example_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost, http://127.0.0.1

DJANGO_SUPERUSER_USERNAME=example_username
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=example_password

WEB_HOST=app
WEB_PORT=8000

NGINX_SERVER_PORT=6060
STATIC_URL=/static/
MEDIA_URL=/media/

DB_PASSWORD=example_password
DB_USER=example_user
DB_HOST=postgres-db
DB_NAME=newsdb

DOMAIN_EMAIL=<leave_empty_if_letsencrypt_is_not_used>
DOMAIN_URL=localhost

TRAEFIK_NAME_TRAEFIK=traefik
TRAEFIK_NAME_APP=app
TRAEFIK_NAME_NGINX=nginx-server

CERTRESOLVER=letsencrypt
```


## Local deploy with http using compose


#### First run

```
sudo make docker-dev-build-run
```

#### Rerun with soft rebuild of web-app service

```
sudo make docker-dev-fast-rerun
```

#### Rerun with docker system prune -af

```
sudo make docker-dev-full-rerun
```


## CI/CD github-runner

#### install

```
sudo adduser runner
```

```
sudo usermod -aG docker runner
```

Use commands from github.repository.settings.runners
Run confing/run commands with prefix: sudo -u runner
Install github-runner to ~/actions-runner/

```
sudo ~/actions-runner/svc.sh install runner
```

```
sudo ~/actions-runner/svc.sh start 
```
