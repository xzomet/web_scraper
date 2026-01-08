from book_scraper.config.settings import (
    CALAOGUE_MAX_FAILURES,
    CATALOGUE_HTML_DIR,
    CATALOGUE_MAPPING_FILE,
)
from book_scraper.scraping.fetcher import fetch_urls_from_mapping


def main():
    fetch_urls_from_mapping(
        CATALOGUE_MAPPING_FILE, CATALOGUE_HTML_DIR, CALAOGUE_MAX_FAILURES
    )


if __name__ == "__main__":
    main()
