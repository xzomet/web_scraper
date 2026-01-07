from book_scraper.models.book import Book
from book_scraper.repo.books_repo import get_book_by_url, insert_book, update_book
from book_scraper.scraping.fetch_catalogue import main as fetch_catalogue_html
from book_scraper.scraping.fetch_details import main as fetch_detail_html
from book_scraper.scraping.parse import catalogue_parser, detail_parser
from book_scraper.scraping.urls import main as generate_html_filenames
from book_scraper.scraping.urls_detail_pages import (
    main as generate_detail_html_filenames,
)


def scrape_catalogue_page() -> list[Book]:
    generate_html_filenames()
    fetch_catalogue_html()
    books = catalogue_parser()
    return books


def scrape_detail_pages() -> list[Book]:
    generate_detail_html_filenames()
    fetch_detail_html()
    books = detail_parser()
    return books


def insert_or_update_books(books: list[Book]) -> None:
    for book in books:
        existing = get_book_by_url(book.url)
        if existing is None:
            insert_book(book)
        else:
            book.id = existing.id
            update_book(book)


# def main():
#     books = scrape_catalogue_page()
#     for book in books:
#         existing = get_book_by_url(book.url)
#         if existing is None:
#             insert_book(book)
#         else:
#             book.id = existing.id
#             update_book(book)


# if __name__ == "__main__":
#     main()
