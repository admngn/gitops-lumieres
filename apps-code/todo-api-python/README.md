# Todo API — Python

[![CI/CD](https://github.com/Akasam/todo-api-python-test/actions/workflows/ci.yml/badge.svg)](https://github.com/Akasam/todo-api-python-test/actions/workflows/ci.yml)

A simple CRUD Todo API built with FastAPI, SQLAlchemy and SQLite.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Run

```bash
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

## Test

```bash
pytest --cov=. --cov-report=html
```

## Docker

```bash
docker build -t todo-api .
docker run -p 8000:8000 todo-api
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/todos` | Create a todo |
| GET | `/todos` | List todos (`?skip=0&limit=10`) |
| GET | `/todos/:id` | Get a todo |
| PUT | `/todos/:id` | Update a todo |
| DELETE | `/todos/:id` | Delete a todo |
