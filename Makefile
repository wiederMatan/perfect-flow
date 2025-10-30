.PHONY: help build up down restart logs shell test lint format clean

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - View logs from all services"
	@echo "  make shell    - Open shell in worker container"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Run linting"
	@echo "  make format   - Format code"
	@echo "  make clean    - Clean up containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started. Prefect UI available at http://localhost:4200"

down:
	docker-compose down

restart: down up

logs:
	docker-compose logs -f

logs-server:
	docker-compose logs -f prefect-server

logs-worker:
	docker-compose logs -f prefect-worker

shell:
	docker-compose exec prefect-worker /bin/bash

shell-server:
	docker-compose exec prefect-server /bin/bash

test:
	docker-compose exec prefect-worker pytest

test-local:
	pytest

lint:
	docker-compose exec prefect-worker ruff check .

format:
	docker-compose exec prefect-worker ruff format .

clean:
	docker-compose down -v
	docker system prune -f

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install ruff black isort mypy

# Prefect specific commands
prefect-deploy:
	docker-compose exec prefect-worker python deployments/deploy_example.py

prefect-run:
	docker-compose exec prefect-worker python flows/example_flow.py

prefect-ui:
	@echo "Opening Prefect UI at http://localhost:4200"
	@open http://localhost:4200 || xdg-open http://localhost:4200
