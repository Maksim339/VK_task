#!/bin/bash

while ! pg_isready -h db -p 5432 -q; do
    sleep 2
done

alembic revision --autogenerate
alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 80
