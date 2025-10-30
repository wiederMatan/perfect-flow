"""Tests for example flow."""

import pytest
from flows.example_flow import fetch_data, process_data, save_results


@pytest.mark.asyncio
async def test_fetch_data():
    """Test fetching data from API."""
    url = "https://jsonplaceholder.typicode.com/posts/1"
    result = await fetch_data(url)

    assert isinstance(result, dict)
    assert "id" in result
    assert "title" in result


def test_process_data():
    """Test data processing."""
    sample_data = [{"id": 1}, {"id": 2}]
    result = process_data(sample_data)

    assert isinstance(result, dict)
    assert result["count"] == 2
    assert result["data"] == sample_data


def test_save_results():
    """Test saving results."""
    sample_data = {"count": 5, "data": []}

    # Should not raise any exceptions
    save_results(sample_data)
