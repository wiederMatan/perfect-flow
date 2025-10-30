"""Example Prefect flow demonstrating basic concepts."""

from prefect import flow, task
from prefect.logging import get_run_logger
import httpx


@task(retries=3, retry_delay_seconds=10)
async def fetch_data(url: str) -> dict:
    """Fetch data from an API endpoint.

    Args:
        url: The URL to fetch data from

    Returns:
        The JSON response as a dictionary
    """
    logger = get_run_logger()
    logger.info(f"Fetching data from {url}")

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


@task
def process_data(data: dict) -> dict:
    """Process the fetched data.

    Args:
        data: The raw data to process

    Returns:
        Processed data
    """
    logger = get_run_logger()
    logger.info("Processing data")

    # Example processing logic
    processed = {
        "count": len(data) if isinstance(data, list) else 1,
        "data": data
    }

    return processed


@task
def save_results(data: dict) -> None:
    """Save processed results.

    Args:
        data: The processed data to save
    """
    logger = get_run_logger()
    logger.info(f"Saving results: {data.get('count', 0)} items")

    # In a real scenario, you would save to a database or file
    logger.info("Results saved successfully")


@flow(name="example-etl-flow", log_prints=True)
async def example_etl_flow(api_url: str = "https://jsonplaceholder.typicode.com/posts"):
    """Example ETL flow that fetches, processes, and saves data.

    Args:
        api_url: The API endpoint to fetch data from
    """
    logger = get_run_logger()
    logger.info("Starting ETL flow")

    # Fetch data
    raw_data = await fetch_data(api_url)

    # Process data
    processed_data = process_data(raw_data)

    # Save results
    save_results(processed_data)

    logger.info("ETL flow completed successfully")
    return processed_data


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_etl_flow())
