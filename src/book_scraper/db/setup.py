import sqlite3
from typing import Any, List, Tuple

from book_scraper.db.database import Database
from book_scraper.models.book import Book
from book_scraper.scraping.parse import main as generate_books


def create_books_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            list_price REAL,
            availability BOOLEAN DEFAULT TRUE,
            rating INTEGER CHECK (rating >= 0 AND rating <= 5),
            scraped_at TEXT NOT NULL
        )
    """
    )


def books_to_sql(books: List[Book]) -> List[Tuple[Any, ...]]:
    return [
        (
            b.title,
            b.url,
            b.list_price,
            b.availability,
            b.rating,
            b.scraped_at.isoformat(),
        )
        for b in books
    ]


def insert_into_db(cur: sqlite3.Cursor, books: List[Book]):
    cur.executemany(
        """
        INSERT INTO books (
            title,
            url,
            list_price,
            availability,
            rating,
            scraped_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        books_to_sql(books),
    )


def main():
    db = Database()
    conn = db.connection
    cur = conn.cursor()

    create_books_table(cur)

    books: List[Book] = generate_books()

    insert_into_db(cur, books)

    conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
