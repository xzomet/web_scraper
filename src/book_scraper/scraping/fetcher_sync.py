import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from tqdm import tqdm

from book_scraper.config.settings import (
    DEFAULT_HEADERS,
    HTML_DIR,
    MAX_RETRIES,
    POOL_CONNECTIONS,
    POOL_MAXSIZE,
    REQUESTS_RETRIES,
    REQUESTS_TIMEOUT,
    SLEEP_BETWEEN_REQUESTS,
)

logger = logging.getLogger(__name__)


class Fetcher:
    def __init__(self, session: requests.Session = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

        adapter = requests.adapters.HTTPAdapter(
            pool_connections=POOL_CONNECTIONS,
            pool_maxsize=POOL_MAXSIZE,
            max_retries=REQUESTS_RETRIES,
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type, exc_value: Exception, traceback) -> None:
        self.session.close()

    def fetch(self, url: str) -> str:
        if not validate_url(url):
            raise ValueError(f"Invalid URL: {url}")

        response = self.session.get(url, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        return response.text

    def fetch_with_retries(self, url: str, retries: int = MAX_RETRIES) -> str:
        """
        Fetch a URL with retry semantics.

        Returns:
            HTML content as a string.

        Raises:
            requests.RequestException: if all retry attempts fail.
            ValueError: if the URL is invalid.
        """
        for attempt in range(retries):
            try:
                return self.fetch(url)
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    raise
        raise RuntimeError("fetch_with_retries reached unreachable code")


def validate_url(url: str) -> bool:
    try:
        u = urlparse(url)
        return all([u.scheme, u.netloc])
    except Exception:
        return False


def load_mapping_file(path: Path) -> List[Dict[str, str]]:
    """Load mapping file from JSON."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_html(filename: str, content: str) -> None:
    """Save HTML content to a file."""
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    file_path = HTML_DIR / filename
    with file_path.open("w", encoding="utf-8") as f:
        f.write(content)


def fetch_urls_from_mapping(path: Path) -> None:
    """
    Fetch all URLs listed in a mapping file and persist HTML to disk.

    Side effects:
        - Reads JSON mapping file at `path`
        - Writes HTML files into HTML_DIR
        - Performs network requests
        - Sleeps between requests

    Raises:
        json.JSONDecodeError: If mapping file is invalid.
        requests.RequestException: If a request fails after retries.
    """
    mapping = load_mapping_file(path)

    with Fetcher() as fetcher:
        logger.info("Starting build...")
        for entry in tqdm(mapping, "Fetching"):
            url = entry.get("url")
            filename = entry.get("filename")

            if not url or not filename:
                logger.warning(f"Invalid entry in mapping file: {entry}")
                continue

            file_path = HTML_DIR / filename

            if file_path.exists() and file_path.stat().st_size > 0:
                logger.debug("File %s already exists. Skipping fetch.", filename)
                continue

            try:
                html_content = fetcher.fetch_with_retries(url)
                save_html(filename, html_content)
                time.sleep(SLEEP_BETWEEN_REQUESTS)
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {e}")
    logger.info("Build complete. %d files fetched and saved.", len(mapping))
