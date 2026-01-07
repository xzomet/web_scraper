import logging
from datetime import datetime

from book_scraper.config.settings import DETAILS_MAPPING_FILE
from book_scraper.scraping.fetcher import fetch_urls_from_mapping

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting fetch of detail pages at %s", datetime.now().isoformat())
    fetch_urls_from_mapping(DETAILS_MAPPING_FILE)
    logger.info("Completed fetch of detail pages at %s", datetime.now().isoformat())


if __name__ == "__main__":
    main()
