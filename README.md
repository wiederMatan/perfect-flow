# Perfect Flow

A Prefect-based workflow orchestration project using Prefect 3 with Python 3.14 and Kubernetes support.

## Overview

Perfect Flow is a workflow orchestration platform built on Prefect 3, designed to manage and schedule data pipelines, ETL processes, and automated workflows.

## Prerequisites

- Docker and Docker Compose
- Python 3.14+ (for local development)
- Make (optional, for convenience commands)

## Quick Start

1. **Clone and setup environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start services**
   ```bash
   make up
   # or
   docker-compose up -d
   ```

3. **Access Prefect UI**
   Open http://localhost:4200 in your browser

4. **Run example flow**
   ```bash
   make prefect-run
   # or
   docker-compose exec prefect-worker python flows/example_flow.py
   ```

## Project Structure

```
perfect-flow/
├── flows/              # Prefect flow definitions
├── deployments/        # Deployment scripts
├── config/            # Configuration files
├── utils/             # Utility functions
├── tests/             # Test files
├── docker-compose.yml # Docker services configuration
├── Dockerfile         # Application container
├── prefect.yaml       # Prefect deployment configuration
└── requirements.txt   # Python dependencies
```

## Development

### Running Tests
```bash
make test              # Run tests in Docker
make test-local        # Run tests locally
```

### Code Quality
```bash
make lint             # Check code style
make format           # Format code
```

### Deployment
```bash
make prefect-deploy   # Deploy flows to Prefect
```

## Services

- **Prefect Server**: Web UI and API (port 4200)
- **Prefect Worker**: Flow execution agent
- **PostgreSQL**: Database backend (port 5432)

## Common Commands

See `make help` for all available commands or refer to CLAUDE.md for detailed development guidance.
