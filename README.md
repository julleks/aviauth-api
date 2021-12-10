# aviauth-api
[![Release Version](https://img.shields.io/github/v/release/julleks/aviauth-api.svg?sort=semver)](https://github.com/julleks/aviauth-api/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/julleks/aviauth-api/blob/develop/LICENSE)
[![CI](https://github.com/julleks/aviauth-api/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/julleks/aviauth-api/actions?query=branch%3A+master)
[![codecov](https://codecov.io/gh/julleks/aviauth-api/branch/master/graph/badge.svg)](https://codecov.io/gh/julleks/aviauth-api)

Authentication microservice based on FastAPI


# Installation guide

Clone the repository
```shell
git clone https://github.com/julleks/aviauth-api/
```

Install [pyenv](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) and dependencies (macOS)
```shell
brew install openssl readline sqlite3 xz zlib

curl https://pyenv.run | bash

pyenv install 3.10.1
```

Install [poetry](https://python-poetry.org)
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

source $HOME/.poetry/env
```

```shell
cd aviauth-api

pyenv local 3.10.1

poetry install

peotry shell
```

Install pre-commit
```shell
pre-commit install
```

Run the application
```shell
./start.sh
```

OpenAPI schema is available at:
```
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

### List of the environmental variables used in project:


| Variable               | Default value     | Is required | Description                               |
| ---------------------- | ----------------- |:-----------:| ----------------------------------------- |
| POSTGRES_DB            | aviauth           | No          |                                           |
| POSTGRES_HOST          | 127.0.0.1         | No          |                                           |
| POSTGRES_PORT          | 5432              | No          |                                           |
| POSTGRES_USER          |                   | Yes         |                                           |
| POSTGRES_PASSWORD      |                   | Yes         |                                           |



### TODO:
- install [bandit](https://bandit.readthedocs.io/en/latest/) for security issues check
- investigate and add more [pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks)


# Hints & Tips

### Commits

[Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) specification

Common commit types:

`feat:`
`fix:`
`build:`
`chore:`
`ci:`
`docs:`
`style:`
`refactor:`
`perf:`
`test:`


###Alembic

Initialize Alembic:
```shell
alembic init -t async migrations
```

Make migration:
```shell
alembic revision --autogenerate -m "migration massage"
```

Apply migration:
```shell
alembic upgrade head
```



# Overview

This project provides authentication and authorization service for external applications.
It allows using other applications without storing any user data in them.

Keeping all the data in a single place and clear management of access permissions for each
authorized application is a goal of this project.

We can end up with 3 products:
- Independent application for integration with external apps
- Open source authentication microservice ready-to-use
- Pip package for FASTApi


### Problem Statement

Most of the web application require registration or authentication using external services 
(as google or facebook), that have almost unlimited access to users data. Easy management of 
applications and permissions they have is something that missing.
Personal data is not personal anymore.


### Proposed Solution

Implement a service that keeps all the user's data encrypted and providing it
to external applications based on configured permissions.


# Success Criteria

- Running application in production environment
- Allowing to perform any user story described below
- Compliance with all requirements of the project


# User Stories

- Register accounts
- CRUD operations on user data
- Several emails / phone numbers / avatars per user
- Register / Manage applications
- Generate authentication tokens (multiple tokens per app)
- Manage permissions per app
- List / Delete active tokens
- See access history
- [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication)


# Scope

- Only creation of the API is the scope of the project. No frontend or other UI is required.
- A service for checking username availability in some popular applications
can be implemented in future iterations.


### Requirements

- [FastAPI](https://fastapi.tiangolo.com) web framework
- [SQLAlchemy](https://www.sqlalchemy.org) ORM
- Test coverage with [pytest](https://docs.pytest.org/en/6.2.x/contents.html)
- [OpenAPI](https://swagger.io/specification/) specification
- [GitHub actions](https://github.com/features/actions) as CI/CD tool
- [AWS](http://aws.amazon.com) infrastructure
- Managing infrastructure with [Terraform](https://www.terraform.io)
- [Trunk-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development)
- [Open Source](https://opensource.org)
- [REST](https://restfulapi.net) API
- [PostgreSQL](https://www.postgresql.org)


### Non-Requirements

- 

### Conventions 

- [Semantic Versioning](https://semver.org/)
- [Changelog](https://keepachangelog.com/en/1.1.0/)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)


### Under discussion

- Blockchain usage
- Data encryption
- Project structure
- [Clean architecture](https://breadcrumbscollector.tech/python-the-clean-architecture-in-2021/)
- Automatic changelog generation
- Automatic versioning / tagging
