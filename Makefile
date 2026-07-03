.PHONY: help setup start stop bash test coverage lint format typecheck arch-check qa migrate

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

setup: ## Build containers and install dependencies
	docker compose build
	docker compose run --rm api uv pip install --system -e ".[dev]"

start: ## Start all containers
	docker compose up -d

stop: ## Stop all containers
	docker compose down

bash: ## Open shell in API container
	docker compose exec api bash

migrate: ## Run database migrations
	docker compose exec api alembic upgrade head

test: ## Run all tests
	docker compose exec api pytest

coverage: ## Run tests with coverage report (90% min)
	docker compose exec api pytest --cov=src --cov-report=html --cov-fail-under=90

lint: ## Lint code with ruff
	docker compose exec api ruff check src tests

format: ## Auto-fix code style
	docker compose exec api ruff format src tests
	docker compose exec api ruff check --fix src tests

typecheck: ## Static type checking with mypy
	docker compose exec api mypy src

arch-check: ## Architecture dependency rules
	docker compose exec api lint-imports

qa: lint typecheck arch-check test ## Full QA suite