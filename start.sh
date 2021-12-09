#!/bin/bash
# Use this script to start the application with hot reload.

uvicorn app.main:app --port 8000 --reload --log-level info
