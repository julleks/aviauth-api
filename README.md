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

Install pre-commit if you are going to make commits to repository
```shell
pre-commit install
```

Set debug to `True` to disable HTTPSRedirectMiddleware locally:
```shell
export DEBUG=True
```

Run the application
```shell
./start.sh
```

OpenAPI schema is available at:
```
http://127.0.0.1:8000/latest/docs
http://127.0.0.1:8000/latest/redoc
http://127.0.0.1:8000/latest/openapi.json
```

### List of the environmental variables used in project:


| Variable          | Default value     | Description                                                                         |
|-------------------|-------------------|-------------------------------------------------------------------------------------|
| POSTGRES_DB       | aviauth           |                                                                                     |
| POSTGRES_HOST     | 127.0.0.1         |                                                                                     |
| POSTGRES_PORT     | 5432              |                                                                                     |
| POSTGRES_USER     |                   |                                                                                     |
| POSTGRES_PASSWORD |                   |                                                                                     |
| DEBUG             | False             | If set to True, logs to console SQL queries and disable HTTPSRedirectMiddleware.    |
| SECRET_KEY        |                   |                                                                                     |
| SENDGRID_API_KEY  |                   |                                                                                     |


### List of the environmental variables used for deployment:

| Variable              | Environment | Description                                           |
|-----------------------|-------------|-------------------------------------------------------|
| AWS_S3_BUCKET         | docs        | S3 bucket name for docs site sync.                    |
| DISTRIBUTION          | docs        | CloudFront distribution ID for cache invalidation.    |
| AWS_ACCESS_KEY_ID     |             | Access key with S3 and CloudFront access permissions. |
| AWS_SECRET_ACCESS_KEY |             |                                                       |
| CODECOV_TOKEN         |             | Required for private repositories only.               |


# Hints & Tips

### Commits

This project is following [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) specification
and [Trunk-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development)
flow.

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

Branch name patterns:

`master`
`feature/{feature_name}`
`bugfix/{hotfix_name}`

#### Before committing, ensure that you have:

* installed pre-commit hook (`pre-commit install`)
* included all the changes to the [CHANGELOG.md](CHANGELOG.md) under
`Unreleased` section
* created a branch according to the pattern described above (e.g.: `feature/{feature_name}`)
* put a correct commit type according to presented above (e.g.: `feat: add new feature`)
* put `!` after the commit type (e.g.: `feat!: and new breaking change`) and place
`BRAKING CHANGE:` in the beginning of commit body (optional)
if you are introducing breaking changes

#### Before the release:

* Set proper release version in the [CHANGELOG.md](CHANGELOG.md)
* Ensure that [CHANGELOG.md](CHANGELOG.md) content is up-to-date
* Set the release date in the [CHANGELOG.md](CHANGELOG.md)
* Update `V{current_major}_VERSION` parameter in [config](app/core/config.py)
according to the releasing one or create a new one if `BREAKING CHANGES`
took place
* Update documentation according to the latest changes.
* Check that `LATEST_VERSION` is pointing to the correct major version parameter in
[config](app/core/config.py)
* After `master` branch is up-to-date, create a release on GitHub including the
latest release notes

### Alembic

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

Downgrade 1 revision:
```shell
alembic downgrade -1
```

### Terraform

Plan changes
```shell
cd infrastructure/aws
./terraform.sh aws-profile-name plan
```

Apply changes
```shell
cd infrastructure/aws
./terraform.sh aws-profile-name apply
```

Import to state
```shell
cd infrastructure/aws
./import.sh aws-profile-name module.module-name module-id
```

### Security

Generate random secret key:
```shell
openssl rand -hex 32
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
