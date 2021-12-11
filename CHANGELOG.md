# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Changelog Convention](https://keepachangelog.com/en/1.0.0/).
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/julleks/aviauth-api/compare/0.1.0...master)

### Added 

* Specify project requirements
* Configure CI workflow to run tests with [pytest](https://docs.pytest.org/en/6.2.x/) using project versions
  of python and poetry on both Linux and macOS
* Add a step to CI workflow to upload [coverage report](https://pytest-cov.readthedocs.io/en/latest/) to [codecov.io](https://app.codecov.io/)
* Install pre-commit hook: [check-builtin-literals](https://github.com/pre-commit/pre-commit-hooks#check-builtin-literals)
* Install pre-commit hook: [check-docstring-first](https://github.com/pre-commit/pre-commit-hooks#check-docstring-first)
* Install pre-commit hook: [check-yaml](https://github.com/pre-commit/pre-commit-hooks#check-yaml)
* Install pre-commit hook: [check-toml](https://github.com/pre-commit/pre-commit-hooks#check-toml)
* Install pre-commit hook: [detect-private-key](https://github.com/pre-commit/pre-commit-hooks#detect-private-key)
* Install pre-commit hook: [end-of-file-fixer](https://github.com/pre-commit/pre-commit-hooks#end-of-file-fixer)
* Create an entrypoint for [FastAPI application](https://fastapi.tiangolo.com)
* Create dependency function to start database session
* Create configuration class
* Install [SQLModel](https://sqlmodel.tiangolo.com/features/) package
* Setup [Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations
* Install [structlog](https://www.structlog.org/en/stable/)

## [0.1.0](https://github.com/julleks/aviauth-api/commits/0.1.0) - 2021-12-08

### Added

* Setup [poetry](https://python-poetry.org) environment manager
* Install [pre-commit](https://pre-commit.com)
* Install pre-commit hook: [black](https://github.com/psf/black)
* Install pre-commit hook: [isort](https://github.com/timothycrosley/isort)
* Install pre-commit hook: [flake-8](https://flake8.pycqa.org/en/latest/)
* Install pre-commit hook: [commitizen](https://commitizen-tools.github.io/commitizen/)
* Configure [dependabot](https://help.github.com/github/administering-a-repository/configuration-options-for-dependency-updates)
