from fastapi import FastAPI
import toml

project_config = toml.load("pyproject.toml")

name = project_config["tool"]["poetry"]["name"]
version = project_config["tool"]["poetry"]["version"]

app = FastAPI(
    title=name,
    version=version,
)
