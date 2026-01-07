import json
from pathlib import Path

import pytest

from book_scraper.models.book import Book
from book_scraper.scraping.parse import catalogue_parser, detail_parser

TEST_DIR = Path("fixtures").resolve()


def test_detail_parser_create_books(monkeypatch, tmp_path):

    # Arrenge

    mapping = [
        {
            "filename": "detail_page.html",
            "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        }
    ]
    html_dir = TEST_DIR

    monkeypatch.setattr(
        "book_scraper.scraping.parse.HTML_DIR",
        html_dir,
    )
    monkeypatch.setattr(
        "book_scraper.scraping.parse.DETAILS_MAPPING_FILE",
        tmp_path / "mapping.json",
    )

    (tmp_path / "mapping.json").write_text(json.dumps(mapping))

    # Act

    books = detail_parser()

    # Assert

    assert len(books) == 1
    book = books[0]

    assert book.url
    assert book.upc
    assert book.price_excl_tax
    assert book.description


def test_catalogue_parser_create_books(monkeypatch, tmp_path):

    # Arrenge

    mapping = [{"filename": "catalogue_page.html"}]
    html_dir = TEST_DIR

    monkeypatch.setattr(
        "book_scraper.scraping.parse.HTML_DIR",
        html_dir,
    )
    monkeypatch.setattr(
        "book_scraper.scraping.parse.CATALOGUE_MAPPING_FILE",
        tmp_path / "mapping.json",
    )

    (tmp_path / "mapping.json").write_text(json.dumps(mapping))

    # Act

    books = catalogue_parser()

    # Assert

    assert books
    assert all(isinstance(b, Book) for b in books)

    for book in books:
        assert book.url
        assert book.title
        assert book.scraped_at
