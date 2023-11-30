#!/bin/bash

cd /app

# Run the Alembic migration
alembic revision --autogenerate -m "init migration"
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
