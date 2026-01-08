"""
Create deterministic HTML filenames for detail URLs.

Each catalogue URL is hashed (SHA-256) to produce a filesystem-safe
HTML filename. The mapping is written to data.json.
"""

import logging
from typing import List

from book_scraper.config.settings import DETAILS_MAPPING_FILE
from book_scraper.repo.books_repo import get_all_books
from book_scraper.scraping.urls import build_mapping, write_json

logger = logging.getLogger(__name__)


def build_detail_urls() -> List[str]:
    books = get_all_books()
    book = books[0]
    logger.info("DETAIL URL: %s", book.url)
    return [book.url for book in books]


def main() -> None:
    logger.info("Starting build.")

    url_list = build_detail_urls()
    logger.info("%d detail urls listed.", len(url_list))

    data = build_mapping(url_list)
    logger.debug("Example mapping: %s", data[0])

    write_json(data, DETAILS_MAPPING_FILE)
    logger.info("Build complete.")


if __name__ == "__main__":
    main()
