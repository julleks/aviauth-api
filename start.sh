#!/bin/bash

# Apply migrations
alembic upgrade head

# Start the application with hot reload.
uvicorn app.main:app --port 8000 --reload --log-level info
