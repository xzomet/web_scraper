import logging
from sqlite3 import Cursor

from book_scraper.db.database import Database

logger = logging.getLogger(__name__)


def create_books_table(cur: Cursor) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            list_price REAL,
            availability BOOLEAN DEFAULT TRUE,
            rating INTEGER CHECK (rating >= 0 AND rating <= 5),
            category TEXT,
            description TEXT,
            thumbnail_url TEXT,
            upc TEXT,
            price_excl_tax FLOAT,
            price_incl_tax FLOAT,
            tax FLOAT,
            availability_count INTEGER,
            num_reviews INTEGER,
            scraped_at TEXT NOT NULL
        )
    """
    )

    logger.info("Ensured books table exists")


def main() -> None:
    with Database() as conn:
        cur = conn.cursor()
        create_books_table(cur)


if __name__ == "__main__":
    main()
