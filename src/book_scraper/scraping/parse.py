"""
HTML parsing layer.

Responsibilities:
- Load HTML files referenced by mapping files
- Parse catalogue and detail HTML into Book domain objects
- Log parsing progress and failures

This module performs no database access and no network IO.

"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from book_scraper.config.settings import (
    CATALOGUE_MAPPING_FILE,
    DETAILS_MAPPING_FILE,
    HTML_DIR,
)
from book_scraper.models.book import Book
from book_scraper.scraping.book_builder import BookBuilder

logger = logging.getLogger(__name__)


# ---------- low-level IO helpers ----------


def load_mapping(path: Path) -> List[Dict[str, str]]:
    """
    Load a JSON mapping file.

    Raises:
        json.JSONDecodeError
        FileNotFoundError
    """
    logger.debug("Loading mapping file: %s", path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_html(path: Path) -> str:
    """
    Read an HTML file from disk.

    Raises:
        FileNotFoundError
        UnicodeDecodeError
    """
    logger.debug("Reading HTML file: %s", path)
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def parse_catalogue_pod(pod: Tag) -> Optional[Book]:
    """
    Parse a single catalogue pod into a Book.

    Returns:
        Book if parsing succeeds, None if required data is missing.
    """
    builder = BookBuilder().with_catalogue_pod(pod)
    return builder.build()


# ---------- catalogue parsing  ----------


def catalogue_parser() -> List[Book]:
    """
    Parse all catalogue HTML files into Book objects.

    Returns:
        List of partially populated Book objects.
    """
    mapping = load_mapping(CATALOGUE_MAPPING_FILE)
    books: List[Book] = []

    logger.info("Starting catalogue parsing")

    for entry in mapping:
        filename = entry["filename"]
        path = HTML_DIR / filename

        logger.debug("Parsing catalogue file: %s", filename)

        try:
            html = read_html(path)
        except Exception:
            logger.exception("Failed to read catalogue HTML: %s", filename)
            continue

        soup = BeautifulSoup(html, "lxml")
        pods = soup.select("article.product_pod")

        logger.debug("Found %d product pods in %s", len(pods), filename)

        for pod in pods:
            book = parse_catalogue_pod(pod)
            if book is None:
                logger.warning("Failed to parse catalogue pod in %s", filename)
                continue
            books.append(book)

    logger.info("Catalogue parsing complete: %d books parsed", len(books))

    return books


def parse_detail_html(html: str, url: str) -> Optional[Book]:
    """
    Parse a detail page HTML into a Book.

    Returns:
        Book if parsing succeeds, None otherwise.
    """
    builder = BookBuilder().with_detail_html(html, url)
    return builder.build()


def detail_parser() -> List[Book]:
    """
    Parse all detail HTML files into Book objects.

    Returns:
        List of enriched Book objects.
    """
    logger.info("Starting detail parsing")
    mapping = load_mapping(DETAILS_MAPPING_FILE)
    books: List[Book] = []

    for entry in mapping:
        filename = entry.get("filename")
        url = entry["url"]
        path = HTML_DIR / entry["filename"]

        logger.debug("Parsing detail file: %s", filename)

        try:
            html = read_html(path)
        except Exception:
            logger.exception("Failed to read detail HTML: %s", filename)
            continue

        book = parse_detail_html(html, url)

        if book is None:
            logger.warning("Failed to parse detail page: %s", filename)
            continue
        books.append(book)
    logger.info("Detail parsing complete: %d books parsed", len(books))
    return books
