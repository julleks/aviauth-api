# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Changelog Convention](https://keepachangelog.com/en/1.0.0/).
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0](https://github.com/julleks/aviauth-api/compare/0.1.0...0.2.0) - 2021-12--27

### Added 

* Specify project requirements by [@rozumalex](https://github.com/rozumalex)
* Configure CI workflow to run tests with [pytest](https://docs.pytest.org/en/6.2.x/) using project versions
  of python and poetry on both Linux and macOS by [@rozumalex](https://github.com/rozumalex)
* Add a step to CI workflow to upload [coverage report](https://pytest-cov.readthedocs.io/en/latest/) to [codecov.io](https://app.codecov.io/) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [check-builtin-literals](https://github.com/pre-commit/pre-commit-hooks#check-builtin-literals) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [check-docstring-first](https://github.com/pre-commit/pre-commit-hooks#check-docstring-first) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [check-yaml](https://github.com/pre-commit/pre-commit-hooks#check-yaml) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [check-toml](https://github.com/pre-commit/pre-commit-hooks#check-toml) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [detect-private-key](https://github.com/pre-commit/pre-commit-hooks#detect-private-key) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [end-of-file-fixer](https://github.com/pre-commit/pre-commit-hooks#end-of-file-fixer) by [@rozumalex](https://github.com/rozumalex)
* Create an entrypoint for [FastAPI application](https://fastapi.tiangolo.com) by [@rozumalex](https://github.com/rozumalex)
* Create dependency function to start database session by [@rozumalex](https://github.com/rozumalex)
* Create configuration class by [@rozumalex](https://github.com/rozumalex)
* Install [SQLModel](https://sqlmodel.tiangolo.com/features/) package by [@rozumalex](https://github.com/rozumalex)
* Setup [Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations by [@rozumalex](https://github.com/rozumalex)
* Install [structlog](https://www.structlog.org/en/stable/) by [@rozumalex](https://github.com/rozumalex)
* Add a list of allowed [CORS origins](https://fastapi.tiangolo.com/tutorial/cors/) by [@rozumalex](https://github.com/rozumalex)
* Configure application for versioning by [@rozumalex](https://github.com/rozumalex)
* Integrate documentation with [readthedocs](https://docs.readthedocs.io/en/stable/tutorial/) by [@rozumalex](https://github.com/rozumalex)
* Implement API for authentication by [@rozumalex](https://github.com/rozumalex)
* Implement API for user registration by [@rozumalex](https://github.com/rozumalex)
* Implement API for retrieving user profile by [@rozumalex](https://github.com/rozumalex)
* Implement basic API for applications registration by [@rozumalex](https://github.com/rozumalex)
* Implement basic scope-based permissions by [@rozumalex](https://github.com/rozumalex)
* Add HTTPSRedirectMiddleware by [@rozumalex](https://github.com/rozumalex)
* Add TrustedHostMiddleware by [@rozumalex](https://github.com/rozumalex)

## [0.1.0](https://github.com/julleks/aviauth-api/commits/0.1.0) - 2021-12-08

### Added

* Setup [poetry](https://python-poetry.org) environment manager by [@rozumalex](https://github.com/rozumalex)
* Install [pre-commit](https://pre-commit.com) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [black](https://github.com/psf/black) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [isort](https://github.com/timothycrosley/isort) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [flake-8](https://flake8.pycqa.org/en/latest/) by [@rozumalex](https://github.com/rozumalex)
* Install pre-commit hook: [commitizen](https://commitizen-tools.github.io/commitizen/) by [@rozumalex](https://github.com/rozumalex)
* Configure [dependabot](https://help.github.com/github/administering-a-repository/configuration-options-for-dependency-updates) by [@rozumalex](https://github.com/rozumalex)
