# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Perfect Flow is a workflow orchestration platform built on **Prefect 3** with Python 3.14, designed for Kubernetes deployments. The project uses Docker for containerization and PostgreSQL for persistence.

## Architecture

### Core Components

- **Prefect Server**: Central orchestration server providing the API and web UI
- **Prefect Worker**: Executes flows pulled from the work pool
- **PostgreSQL**: Stores flow run metadata, deployment configurations, and state
- **Flows**: Python modules in `flows/` containing workflow definitions decorated with `@flow`
- **Tasks**: Reusable units of work within flows, decorated with `@task`
- **Deployments**: Scripts in `deployments/` that register flows with the server

### Project Structure

```
flows/              - Flow definitions (business logic)
deployments/        - Deployment scripts to register flows with Prefect
config/            - Application settings using Pydantic BaseSettings
utils/             - Shared utilities (logging, helpers)
tests/             - Pytest test suite
.prefect/          - Local Prefect storage (gitignored)
```

### Configuration System

Settings are managed through `config/settings.py` using Pydantic Settings:
- Environment variables loaded from `.env` file
- Access via `from config import settings`
- Database URL constructed automatically from components
- Settings include Prefect API URL, database credentials, log level

## Development Commands

### Docker Operations

```bash
# Start all services (Prefect server, worker, PostgreSQL)
make up
docker-compose up -d

# View logs
make logs                    # All services
make logs-server            # Prefect server only
make logs-worker            # Worker only

# Stop services
make down

# Rebuild containers
make build

# Access container shell
make shell                  # Worker container
make shell-server          # Server container
```

### Testing

```bash
# Run tests in Docker environment
make test
docker-compose exec prefect-worker pytest

# Run tests locally (requires local Python environment)
make test-local
pytest

# Run specific test file
pytest tests/test_example_flow.py

# Run tests with markers
pytest -m asyncio
pytest -m integration
```

### Running Flows

```bash
# Run flow directly (for testing)
make prefect-run
docker-compose exec prefect-worker python flows/example_flow.py

# Deploy flow to Prefect server
make prefect-deploy
docker-compose exec prefect-worker python deployments/deploy_example.py

# Run flow from within worker container
make shell
python flows/example_flow.py
```

### Prefect UI

Access the Prefect web interface at http://localhost:4200 after starting services.

## Creating New Flows

### Flow Structure

All flows should:
1. Be placed in the `flows/` directory
2. Use async/await for I/O operations
3. Include proper logging via `get_run_logger()`
4. Define tasks with retry logic where appropriate
5. Export the flow in `flows/__init__.py`

### Example Flow Pattern

```python
from prefect import flow, task
from prefect.logging import get_run_logger

@task(retries=3, retry_delay_seconds=10)
async def fetch_data(url: str) -> dict:
    logger = get_run_logger()
    logger.info(f"Fetching from {url}")
    # Implementation
    return data

@flow(name="my-flow", log_prints=True)
async def my_flow(param: str):
    logger = get_run_logger()
    logger.info("Starting flow")

    result = await fetch_data(param)
    # Process result

    return result
```

### Deployment Pattern

Create a deployment script in `deployments/`:

```python
from flows.my_flow import my_flow

if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="default-agent-pool",
        cron="0 0 * * *",  # Schedule
        tags=["tag1", "tag2"],
        description="Description",
        version="1.0.0",
    )
```

## Testing Patterns

### Async Tasks

Use `@pytest.mark.asyncio` for async task tests:

```python
@pytest.mark.asyncio
async def test_async_task():
    result = await my_async_task()
    assert result is not None
```

### Synchronous Tasks

Regular pytest functions for sync tasks:

```python
def test_sync_task():
    result = my_sync_task()
    assert result == expected
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Required for connecting to Prefect server
PREFECT_API_URL=http://localhost:4200/api

# Database configuration (matches docker-compose.yml)
POSTGRES_USER=prefect
POSTGRES_PASSWORD=prefect
POSTGRES_DB=prefect
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Application settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## Docker Image

Base image: `prefecthq/prefect:3-python3.14-kubernetes`

This image includes:
- Prefect 3.x
- Python 3.14
- Kubernetes integration for K8s deployments
- Pre-configured Prefect CLI

## Work Pools and Agents

- Default work pool: `default-agent-pool`
- Worker starts automatically via docker-compose
- Worker pulls and executes flows from the work pool
- Configure work pools in `prefect.yaml` or via Prefect UI

## Logging

- Prefect flows use `get_run_logger()` for automatic context tracking
- Application utilities can use `utils.setup_logger(name)` for standard logging
- Log level configured via `LOG_LEVEL` environment variable
- Logs visible in Prefect UI and container logs

## Key Differences from Prefect 2.x

If coming from Prefect 2.x:
- Work pools replace agent configurations
- `prefect.yaml` is the main deployment configuration file
- Deployments use `.deploy()` method instead of separate deployment API
- Server start command: `prefect server start` (no separate Orion/Prefect Server distinction)

## Common Workflows

### Adding a New Scheduled Flow

1. Create flow in `flows/my_new_flow.py`
2. Add flow export to `flows/__init__.py`
3. Create deployment script in `deployments/deploy_my_flow.py`
4. Run deployment: `docker-compose exec prefect-worker python deployments/deploy_my_flow.py`
5. Verify in Prefect UI at http://localhost:4200

### Debugging a Failed Flow Run

1. Check Prefect UI for error details and logs
2. View worker logs: `make logs-worker`
3. Check server logs: `make logs-server`
4. Run flow directly for debugging: `make shell` then `python flows/my_flow.py`
5. Add breakpoints and run locally with `python flows/my_flow.py`

### Updating Dependencies

1. Add package to `requirements.txt`
2. Rebuild container: `make build`
3. Restart services: `make restart`

## Database Access

PostgreSQL is accessible at:
- Host: `localhost`
- Port: `5432`
- Database: `prefect`
- User: `prefect`
- Password: `prefect`

Connection string: `postgresql+asyncpg://prefect:prefect@localhost:5432/prefect`
