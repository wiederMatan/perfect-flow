"""Deployment script for example flow."""

from prefect import flow
from flows.example_flow import example_etl_flow


if __name__ == "__main__":
    # Deploy the flow
    example_etl_flow.deploy(
        name="example-etl-deployment",
        work_pool_name="default-agent-pool",
        cron="0 0 * * *",  # Run daily at midnight
        tags=["example", "etl"],
        description="Example ETL flow that runs daily",
        version="1.0.0",
    )

    print("Deployment created successfully!")
