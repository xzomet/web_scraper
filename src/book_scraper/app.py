import logging
from typing import List

from book_scraper.db.setup import main as db_setup
from book_scraper.log_config.setup import setup_logging
from book_scraper.models.book import Book
from book_scraper.repo.books_repo import upsert_book
from book_scraper.scraping.fetch_catalogue import main as fetch_catalogue_html
from book_scraper.scraping.fetch_details import main as fetch_detail_html
from book_scraper.scraping.parse import catalogue_parser, detail_parser
from book_scraper.scraping.urls import main as generate_html_filenames
from book_scraper.scraping.urls_detail_pages import (
    main as generate_detail_html_filenames,
)

logger = logging.getLogger("__main__")


def scrape_catalogue_page() -> List[Book]:

    logger.info("Starting catalogue scrape")

    generate_html_filenames()
    fetch_catalogue_html()
    books = catalogue_parser()

    logger.info("Parsed %d books from catalogue pages", len(books))

    return books


def scrape_detail_pages() -> List[Book]:

    logger.info("Starting detail page scrape")

    generate_detail_html_filenames()
    fetch_detail_html()
    books = detail_parser()

    logger.info("Parsed %d books from detail pages", len(books))

    return books


def insert_or_update_books(books: List[Book]) -> None:
    for book in books:
        upsert_book(book)

    logger.info("Upserted %d books into database", len(books))


def main():

    setup_logging()
    db_setup()

    logger.info("Scraping job started")

    catalogue_books = scrape_catalogue_page()
    insert_or_update_books(catalogue_books)

    detail_books = scrape_detail_pages()
    insert_or_update_books(detail_books)

    logger.info("Scraping job completed successfully")


if __name__ == "__main__":
    main()
