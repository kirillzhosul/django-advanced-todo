# Django Advanced TODO

[![Tests](https://github.com/kirillzhosul/django-advanced-todo/actions/workflows/tests.yml/badge.svg)](https://github.com/kirillzhosul/advanced-todo/actions/workflows/tests.yml) \
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Test task for one of the companies. Django REST TODO on steroids with metrics and subtasks. \
Main goal is to todo simple TODO (REST API) with metrics (analytics) and also stuff like sub-tasks, completion and tracking

## How to try project?

Project is being deployed to staging. You can try project [here](https://kirillzhosul.florgon.com/tests/api/todo) (Click!)
Test user:

- Login: exampleuser
- Password: examplepassword

## Methods?

TBD

## How to run?

Project uses Docker, to run use:

- `git clone https://github.com/kirillzhosul/django-advanced-todo.git`
- `cd django-advanced-todo/src`
- `cp .example.server.env .server.env`
- `docker-compose up`.
  This will run Docker, Database and server with Gunicorn!
  (Please notice to copy)

#### Static files?

Currently in staging, static files is being served by Ngninx (plus Django `collectstatic`)
On the development, static files is avaliable when using django `runserver`

#### Migrations?

Run `docker exec -it django-advanced-todo-server-1 /bin/sh` and then `python manage.py makemigrations && python manage.py migrate` this will trigger all database migrations!

## How to configure?

You can modify environment variables inside `/src/.server.env` file that will be passed to the server with Docker.
Example file can be copied from `/src/.example.server.env`

## Technologies.

- Python / Django (With DRF).
- Gunicorn with Uvicorn workers (ASGI).
- Docker / Docker-Compose
- PostgreSQL / Django ORM
- GitHub Workflows (CI/CD)
- Nginx on the server side as the proxy server.
- Mostly, **Debian** as the staging server

## CI / CD.

- CD: Removed
- CI: Project have tests workflow, that will run Django tests / Test Docker when you are merging branch into `main` branch
  For now there is no special tests written for this project, so tests just not so useful.

## Testing.

Run `docker exec -it django-advanced-todo-1 /bin/sh` and then `python manage.py test` this will trigger all tests!

## References.

- [Deployed version](https://kirillzhosul.florgon.com/tests/api/todo)
