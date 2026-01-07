import logging
from datetime import datetime
from typing import Any, List, Tuple

from book_scraper.db.database import Database
from book_scraper.models.book import Book

logger = logging.getLogger(__name__)


def get_all_books() -> List[Book]:
    """
    Loads all books from the database and returns them as a list of Book objects.
    """
    with Database() as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM books")

        keys = [c[0] for c in cur.description]
        value_list = cur.fetchall()
        books: List[Book] = []

        for values in value_list:
            book_dict = {k: v for k, v in zip(keys, values)}
            book = Book(**book_dict)
            book.scraped_at = datetime.fromisoformat(book.scraped_at)
            books.append(book)

    logger.info(f"Loaded {len(books)} books from the database.")
    return books


def get_book_by_url(url: str) -> Book | None:
    """
    Loads a book from the database by its URL. Returns None if not found.
    """
    with Database() as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM books WHERE url = ?", (url,))
        values = cur.fetchone()

        if not values:
            return None

        keys = [c[0] for c in cur.description]

        book_dict = {k: v for k, v in zip(keys, values)}

        book = Book(**book_dict)

        book.scraped_at = datetime.fromisoformat(book.scraped_at)

    return book


def book_to_sql(book: Book) -> Tuple[Any, ...]:
    return (
        book.title,
        book.url,
        book.list_price,
        book.availability,
        book.rating,
        book.scraped_at.isoformat(),
    )


def insert_book(book: Book) -> Book:
    """
    Inserts a new book into the db and returns Book with id.
    """

    with Database() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO books(
                title,
                url,
                list_price,
                availability,
                rating,
                scraped_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            book_to_sql(book),
        )
        book.id = cur.lastrowid

    return book


def update_book(book: Book) -> None:
    """
    Updates an existing book in the database.
    """

    if book.id is None:
        raise ValueError("Cannot update book without id.")

    with Database() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE books
            SET title = ?,
                url = ?,
                list_price = ?,
                availability = ?,
                rating = ?,
                scraped_at = ?
            WHERE id = ?
            """,
            book_to_sql(book) + (book.id,),
        )


def remove_book(book: Book) -> None:
    if book.id is None:
        raise ValueError("Cannot delete Book without id")

    with Database() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id = ?", (book.id,))
