"""Configuration management for StockAgent."""

import os
from pathlib import Path

from dotenv import load_dotenv


def load_config() -> dict[str, str]:
    """Load configuration from environment variables.

    Loads .env file if present, then reads required environment variables.

    Returns:
        dict with configuration values including POLYGON_API_KEY

    Raises:
        ValueError: If required environment variables are missing
    """
    # Load .env file from project root if it exists
    # Path: config.py -> stockagent -> src -> project_root
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)

    # Get required API key
    polygon_api_key = os.getenv("POLYGON_API_KEY")

    if not polygon_api_key:
        raise ValueError(
            "POLYGON_API_KEY environment variable is required. "
            "Please set it in your .env file or environment. "
            "Get a free API key at https://polygon.io/"
        )

    return {
        "POLYGON_API_KEY": polygon_api_key,
    }


def get_polygon_api_key() -> str:
    """Get the Polygon.io API key.

    Returns:
        The API key string

    Raises:
        ValueError: If API key is not configured
    """
    config = load_config()
    return config["POLYGON_API_KEY"]
