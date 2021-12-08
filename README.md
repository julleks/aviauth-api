# aviauth-api
Authentication microservice based on FastAPI


# Installation guide


Clone the repository
```shell
git clone https://github.com/julleks/aviauth-api/
```


Create virtual environment and install the requirements
```shell
cd aviauth-api
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Install pre-commit
```shell
pre-commit install
```


### TODO:
- install [bandit](https://bandit.readthedocs.io/en/latest/) for security issues check
- investigate and add more [pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks)
