# aviauth-api
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


### TODO:
- install [bandit](https://bandit.readthedocs.io/en/latest/) for security issues check
- investigate and add more [pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks)
