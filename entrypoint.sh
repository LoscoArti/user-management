#!/bin/bash

cd /app

alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000
