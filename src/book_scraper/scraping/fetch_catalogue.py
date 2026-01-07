from book_scraper.config.settings import CATALOGUE_MAPPING_FILE
from book_scraper.scraping.fetcher import fetch_urls_from_mapping


def main():
    fetch_urls_from_mapping(CATALOGUE_MAPPING_FILE)


if __name__ == "__main__":
    main()
