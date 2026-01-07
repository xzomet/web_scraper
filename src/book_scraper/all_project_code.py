# ============================================================================
# COMBINED PROJECT CODE
# Total files: 22
# ============================================================================


================================================================================
# FILE 1/22: allfiles.py
================================================================================

#!/usr/bin/env python3
"""
Collect all Python files in a directory tree and combine them into a single file
with clear headers showing file paths.
"""

import os
import sys
from pathlib import Path

def collect_python_files(root_dir="."):
    """Collect all Python files in the directory tree."""
    python_files = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob("*.py"):
        # Skip __pycache__ directories
        if "__pycache__" in str(file_path):
            continue
        
        # Skip if it's actually a directory (though .py shouldn't be)
        if file_path.is_file():
            python_files.append(file_path)
    
    # Sort files for consistent output
    python_files.sort(key=lambda x: str(x))
    return python_files

def combine_files_to_single(output_file="all_code.py", root_dir="."):
    """Combine all Python files into a single file with headers."""
    python_files = collect_python_files(root_dir)
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("# ============================================================================\n")
        outfile.write("# COMBINED PROJECT CODE\n")
        outfile.write(f"# Total files: {len(python_files)}\n")
        outfile.write("# ============================================================================\n\n")
        
        for i, file_path in enumerate(python_files, 1):
            # Write header
            outfile.write(f"\n{'=' * 80}\n")
            outfile.write(f"# FILE {i}/{len(python_files)}: {file_path}\n")
            outfile.write(f"{'=' * 80}\n\n")
            
            try:
                # Read and write file content
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    outfile.write(content)
                    
                    # Add newline if file doesn't end with one
                    if content and not content.endswith("\n"):
                        outfile.write("\n")
                        
            except Exception as e:
                outfile.write(f"# ERROR reading file: {e}\n\n")
        
        # Write summary
        outfile.write(f"\n{'=' * 80}\n")
        outfile.write("# SUMMARY\n")
        outfile.write(f"# Files combined: {len(python_files)}\n")
        outfile.write("# File list:\n")
        for file_path in python_files:
            outfile.write(f"#   {file_path}\n")
        outfile.write(f"{'=' * 80}\n")
    
    print(f"✓ Combined {len(python_files)} files into '{output_file}'")
    return python_files

def main():
    # If a directory is provided as argument, use it
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = "all_project_code.py"
    
    print(f"Scanning for Python files in: {os.path.abspath(root_dir)}")
    
    try:
        files = combine_files_to_single(output_file, root_dir)
        
        print("\nFiles included:")
        for file_path in files:
            print(f"  {file_path}")
            
        # Print file size
        output_size = os.path.getsize(output_file)
        print(f"\nOutput file size: {output_size:,} bytes ({output_size/1024:.1f} KB)")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

================================================================================
# FILE 2/22: app.py
================================================================================

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

================================================================================
# FILE 3/22: config/__init__.py
================================================================================


================================================================================
# FILE 4/22: config/settings.py
================================================================================

from logging import getLogger
from pathlib import Path
from urllib.parse import urljoin

from book_scraper.logging.setup import setup_logging

setup_logging()
logger = getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
BASE_SITE = "https://books.toscrape.com"
CATALOGUE_SITE = urljoin(BASE_SITE, "catalogue/")
# NUM_PAGES is hardcoded because there are fifty catalogue pages in books.toscrape.com
NUM_PAGES = 50
DATA_DIR = BASE_DIR / "data/"
DATA_DIR.mkdir(parents=True, exist_ok=True)

MAPPING_DIR = DATA_DIR / "mappings"
MAPPING_DIR.mkdir(parents=True, exist_ok=True)

CATALOGUE_MAPPING_DIR = MAPPING_DIR / "catalogue"
CATALOGUE_MAPPING_DIR.mkdir(parents=True, exist_ok=True)
CATALOGUE_MAPPING_FILE = CATALOGUE_MAPPING_DIR / "catalogue_mapping.json"

DETAILS_MAPPING_DIR = MAPPING_DIR / "details"
DETAILS_MAPPING_DIR.mkdir(parents=True, exist_ok=True)
DETAILS_MAPPING_FILE = DETAILS_MAPPING_DIR / "details_mapping.json"

HTML_DIR = DATA_DIR / "html"
HTML_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILE = DATA_DIR / "books.db"

logger.debug("BASE_DIR set to: %s", BASE_DIR)
logger.debug("CATALOGUE_SITE set to: %s", CATALOGUE_SITE)
logger.debug("NUM_PAGES set to: %d", NUM_PAGES)
logger.debug("DATA_FILE set to: %s", DATA_FILE)


# requests settings
REQUESTS_TIMEOUT = 10  # seconds
REQUESTS_RETRIES = 3
SLEEP_BETWEEN_REQUESTS = 0.2  # seconds


POOL_CONNECTIONS = 10
POOL_MAXSIZE = 10
MAX_RETRIES = 3


# User-Agent to mimic a real browser
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

================================================================================
# FILE 5/22: db/__init__.py
================================================================================


================================================================================
# FILE 6/22: db/database.py
================================================================================

import logging
import sqlite3
from pathlib import Path
from typing import Optional

from book_scraper.config.settings import DATA_FILE

logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    pass


class Database:
    # Class variable (shared by all instances)
    _connection: Optional[sqlite3.Connection] = None

    def __init__(self, db_path: Path = DATA_FILE) -> None:
        if not hasattr(self, "_initialized"):
            self._db_path = db_path
            self._db_path.parent.mkdir(parents=True, exist_ok=True)

            self.connection_string = str(self._db_path)

            logger.debug("Database configured at %s", self._db_path)
            self._initialized = True

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(self.connection_string)
                logger.debug("Opening SQLite connection: %s", self._db_path)
            except sqlite3.Error as exc:
                raise DatabaseConnectionError(
                    f"Failed to connect db: {self._db_path}."
                ) from exc
        return self._connection

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> sqlite3.Connection:
        return self.connection

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.close()

================================================================================
# FILE 7/22: db/setup.py
================================================================================

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

================================================================================
# FILE 8/22: logging/__init__.py
================================================================================


================================================================================
# FILE 9/22: logging/setup.py
================================================================================

import logging


def setup_logging(level=logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )

================================================================================
# FILE 10/22: models/__init__.py
================================================================================


================================================================================
# FILE 11/22: models/book.py
================================================================================

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Book:
    # fetched from list pages
    id: Optional[int] = None
    title: str = ""
    url: str = ""
    list_price: Optional[float] = None
    availability: Optional[bool] = None
    rating: Optional[int] = None

    # detail page
    upc: Optional[str] = None
    price_excl_tax: Optional[float] = None
    price_incl_tax: Optional[float] = None
    tax: Optional[float] = None
    availability_count: Optional[int] = None
    num_reviews: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None

    scraped_at: datetime = field(default_factory=datetime.utcnow)

================================================================================
# FILE 12/22: repo/__init__.py
================================================================================


================================================================================
# FILE 13/22: repo/books_repo.py
================================================================================

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

================================================================================
# FILE 14/22: scraping/__init__.py
================================================================================


================================================================================
# FILE 15/22: scraping/book_builder.py
================================================================================

from datetime import datetime

from bs4 import Tag

from book_scraper.models.book import Book
from book_scraper.scraping.parse_primitives import (
    parse_availability,
    parse_availability_count,
    parse_category_name,
    parse_description,
    parse_num_reviews,
    parse_price,
    parse_price_excl_tax,
    parse_price_incl_tax,
    parse_product_info,
    parse_rating,
    parse_tax,
    parse_thumbnail_url,
    parse_title,
    parse_url,
)


class BookBuilder:
    def __init__(self) -> None:
        self._data = {}

    def with_catalogue_pod(self, pod: Tag) -> "BookBuilder":
        self._data["url"] = parse_url(pod)
        self._data["title"] = parse_title(pod)
        self._data["price"] = parse_price(pod)
        self._data["rating"] = parse_rating(pod)
        self._data["availability"] = parse_availability(pod)
        return self

    def with_detail_html(self, html: str) -> "BookBuilder":
        self._data["description"] = parse_description(html)
        self._data["category_name"] = parse_category_name(html)
        self._data["thumbnail_url"] = parse_thumbnail_url(html)
        product_info = parse_product_info(html)
        self._data["price_excl_tax"] = parse_price_excl_tax(product_info)
        self._data["price_incl_tax"] = parse_price_incl_tax(product_info)
        self._data["tax"] = parse_tax(product_info)
        self._data["num_reviews"] = parse_num_reviews(product_info)
        self._data["availability_count"] = parse_availability_count(product_info)
        return self

    def build(self) -> Book:
        REQUEIRED_FIELDS = ["url", "title"]
        for field in REQUEIRED_FIELDS:
            if field not in self._data:
                raise ValueError(f"Missing required field: {field}")
        self._data["scraped_at"] = datetime.utcnow()
        return Book(**self._data)

================================================================================
# FILE 16/22: scraping/fetch_catalogue.py
================================================================================

from book_scraper.config.settings import CATALOGUE_MAPPING_FILE
from book_scraper.scraping.fetcher import fetch_urls_from_mapping


def main():
    fetch_urls_from_mapping(CATALOGUE_MAPPING_FILE)


if __name__ == "__main__":
    main()

================================================================================
# FILE 17/22: scraping/fetch_details.py
================================================================================

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

================================================================================
# FILE 18/22: scraping/fetcher.py
================================================================================

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

f
import requests

from book_scraper.config.settings import (
    DEFAULT_HEADERS,
    HTML_DIR,
    MAX_RETRIES,
    POOL_CONNECTIONS,
    POOL_MAXSIZE,
    REQUESTS_RETRIES,
    REQUESTS_TIMEOUT,
    SLEEP_BETWEEN_REQUESTS,
)

logger = logging.getLogger(__name__)


class Fetcher:
    def __init__(self, session: requests.Session = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

        adapter = requests.adapters.HTTPAdapter(
            pool_connections=POOL_CONNECTIONS,
            pool_maxsize=POOL_MAXSIZE,
            max_retries=REQUESTS_RETRIES,
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type, exc_value: Exception, traceback) -> None:
        self.session.close()

    def fetch(self, url: str) -> str:
        if not validate_url(url):
            raise ValueError(f"Invalid URL: {url}")

        response = self.session.get(url, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        return response.text

    def fetch_with_retries(self, url: str, retries: int = MAX_RETRIES) -> Optional[str]:
        for attempt in range(retries):
            try:
                return self.fetch(url)
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    raise


def validate_url(url: str) -> bool:
    try:
        u = urlparse(url)
        return all([u.scheme, u.netloc])
    except Exception:
        return False


def load_mapping_file(path: Path) -> List[Dict[str, str]]:
    """Load mapping file from JSON."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_html(filename: str, content: str) -> None:
    """Save HTML content to a file."""
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    file_path = HTML_DIR / filename
    with file_path.open("w", encoding="utf-8") as f:
        f.write(content)


def fetch_urls_from_mapping(path: Path) -> None:
    mapping = load_mapping_file(path)

    with Fetcher() as fetcher:
        logger.info("Starting build...")
        for entry in mapping:
            url = entry.get("url")
            filename = entry.get("filename")

            if not url or not filename:
                logger.warning(f"Invalid entry in mapping file: {entry}")
                continue

            # path = Path.joinpath(HTML_DIR, filename)
            # if path.exists:
            #     if path.stat().st_size > 0:
            #         logger.debug(f"File {filename} already exists. Skipping.")
            #         continue

            try:
                html_content = fetcher.fetch_with_retries(url)
                save_html(filename, html_content)
                logger.info(f"Fetched and saved {url}")
                time.sleep(SLEEP_BETWEEN_REQUESTS)
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {e}")
    logger.info("Build complete. %d files fetched and saved.", len(mapping))

================================================================================
# FILE 19/22: scraping/parse.py
================================================================================

"""
Module to parse HTML files and extract book information.

"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from bs4.element import Tag

from book_scraper.config.settings import (
    CATALOGUE_MAPPING_FILE,
    CATALOGUE_SITE,
    DETAILS_MAPPING_FILE,
    HTML_DIR,
)
from book_scraper.models.book import Book
from book_scraper.scraping.book_builder import BookBuilder

logger = logging.getLogger(__name__)


def load_mapping(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_html(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def parse_catalogue_pod(pod: Tag) -> Optional[Book]:
    builder = BookBuilder().with_catalogue_pod(pod)
    return builder.build()


def catalogue_parser() -> List[Book]:
    mapping = load_mapping(CATALOGUE_MAPPING_FILE)
    books: List[Book] = []

    for entry in mapping:
        path = HTML_DIR / entry["filename"]

        html = read_html(path)
        soup = BeautifulSoup(html, "lxml")
        pods = soup.select("article.product_pod")

        for pod in pods:
            book = parse_catalogue_pod(pod)
            if book is None:
                continue
            books.append(book)
    return books


def parse_detail_html(html: str) -> Optional[Book]:
    builder = BookBuilder().with_detail_html(html)
    return builder.build()


def detail_parser() -> List[Book]:
    mapping = load_mapping(DETAILS_MAPPING_FILE)
    books: List[Book] = []

    for entry in mapping:
        path = HTML_DIR / entry["filename"]

        html = read_html(path)
        book = parse_detail_html(html)
        if book is None:
            continue
        books.append(book)
    return books


def main() -> List[Book]:
    books = catalogue_parser()
    logger.info(f"Parsed {len(books)} books from HTML files.")

    return books


if __name__ == "__main__":
    main()

================================================================================
# FILE 20/22: scraping/parse_primitives.py
================================================================================

"""
Module for parsing book data from HTML content.
Includes functions to extract information from both catalogue pods and detailed book pages.
"""

import logging
import re
from typing import Dict, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from book_scraper.config.settings import BASE_SITE, CATALOGUE_SITE

# Module-level logger
logger = logging.getLogger(__name__)


# Parsing catalogue pod HTML


def parse_title(pod: Tag) -> Optional[str]:
    """
    Extracts the book title from a catalogue pod.
    """
    title_tag = pod.find("h3").find("a")
    if title_tag and title_tag.has_attr("title"):
        return title_tag["title"].strip()
    logger.warning("Title not found in pod")
    return None


def parse_url(pod: Tag) -> Optional[str]:
    a_tag = pod.select_one("h3 > a")
    if not a_tag:
        logger.error("a_tag doesnt have h3 > a")
        return None
    href = a_tag.get("href")
    if not href:
        logger.error("no href in a_tag")
        return None
    return urljoin(BASE_SITE, href)


def parse_float(value: str) -> Optional[float]:
    m = re.search(r"[\d.,]+", value)
    if not m:
        return None
    return float(m.group(0).replace(",", ""))


def parse_price(pod: Tag) -> Optional[float]:
    p_tag = pod.select_one("p.price_color")
    if not p_tag:
        return None
    if not p_tag.text:
        return None
    return parse_float(p_tag.text)


def parse_rating(pod: Tag) -> Optional[int]:
    rating_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    p_tag = pod.select_one("p.star-rating")
    if not p_tag:
        return None
    if len(p_tag["class"]) < 2:
        return None
    rating_str = p_tag["class"][1]
    return rating_dict.get(rating_str)


def parse_availability(pod: Tag) -> Optional[bool]:
    p_tag = pod.select_one("p.instock")
    if not p_tag:
        return None
    if not p_tag.text:
        return None
    return "In stock" in p_tag.text


# Parsing detail page HTML


def parse_category_name(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")
    un_breadcrumb = soup.select_one("ul.breadcrumb")
    if not un_breadcrumb:
        logger.error("No breadcrumb found in HTML")
        return None
    li_tags = un_breadcrumb.select("li")
    if len(li_tags) < 3:
        logger.error("Breadcrumb does not have enough li tags")
        return None
    category_tag = li_tags[2].select_one("a")
    if not category_tag:
        logger.error("No category link found in breadcrumb")
        return None
    return category_tag.text.strip()


def parse_thumbnail_url(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")
    img_tag = soup.select_one("div.item.active > img")
    if not img_tag:
        logger.error("No image tag found in HTML")
        return None
    src = img_tag.get("src")
    if not src:
        logger.error("No src attribute found in image tag")
        return None
    return urljoin(CATALOGUE_SITE, src)


def parse_description(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")
    desc_header = soup.find("h2", string="Product Description")
    if not desc_header:
        logger.error("No product description header found in HTML")
        return None
    desc_paragraph = desc_header.find_next_sibling("p")
    if not desc_paragraph:
        logger.error("No product description paragraph found in HTML")
        return None
    return desc_paragraph.text.strip()


def parse_product_info(html: str) -> Dict[str, Optional[str]]:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", class_="table table-striped")
    info: Dict[str, Optional[str]] = {}

    if not table:
        logger.error("No product information table found in HTML")
        return info

    for row in table.find_all("tr"):
        header = row.find("th")
        data = row.find("td")
        if header and data:
            info[header.text.strip()] = data.text.strip()
    return info


def parse_upc(product_info: Dict[str, Optional[str]]) -> Optional[str]:
    return product_info.get("UPC")


def parse_price_excl_tax(product_info: Dict[str, Optional[str]]) -> Optional[float]:
    price_str = product_info.get("Price (excl. tax)")
    if price_str:
        return parse_float(price_str)
    return None


def parse_price_incl_tax(product_info: Dict[str, Optional[str]]) -> Optional[float]:
    price_str = product_info.get("Price (incl. tax)")
    if price_str:
        return parse_float(price_str)
    return None


def parse_tax(product_info: Dict[str, Optional[str]]) -> Optional[float]:
    tax_str = product_info.get("Tax")
    if tax_str:
        return parse_float(tax_str)
    return None


def parse_int(value: str) -> Optional[int]:
    m = re.search(r"[\d]+", value)
    if not m:
        return None
    return int(m.group(0))


def parse_availability_count(product_info: Dict[str, Optional[str]]) -> Optional[int]:
    availability_str = product_info.get("Availability")
    if availability_str:
        return parse_int(availability_str)
    return None


def parse_num_reviews(product_info: Dict[str, Optional[str]]) -> Optional[int]:
    reviews_str = product_info.get("Number of reviews")
    if reviews_str and reviews_str.isdigit():
        return int(reviews_str)
    return None

================================================================================
# FILE 21/22: scraping/urls.py
================================================================================

"""
Create deterministic HTML filenames for catalogue URLs.

Each catalogue URL is hashed (SHA-256) to produce a filesystem-safe
HTML filename. The mapping is written to data.json.
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, List

from book_scraper.config.settings import (
    CATALOGUE_MAPPING_FILE,
    CATALOGUE_SITE,
    NUM_PAGES,
)

logger = logging.getLogger(__name__)


def build_catalogue_urls() -> List[str]:
    return [f"{CATALOGUE_SITE}page-{str(i)}.html" for i in range(1, NUM_PAGES + 1)]


def hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def build_mapping(urls: List[str]) -> List[Dict[str, str]]:
    return [{"url": url, "filename": f"{hash_url(url)}.html"} for url in urls]


def write_json(data: List[Dict[str, str]], path: Path) -> None:
    logger.info("Dumping mapping to %s", path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main() -> None:
    logger.info("Starting build.")

    url_list = build_catalogue_urls()
    logger.info("%d catalogue urls listed.", len(url_list))

    data = build_mapping(url_list)
    logger.debug("Example mapping: %s", data[0])

    write_json(data, CATALOGUE_MAPPING_FILE)
    logger.info("Build complete.")


if __name__ == "__main__":
    main()

================================================================================
# FILE 22/22: scraping/urls_detail_pages.py
================================================================================

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

================================================================================
# SUMMARY
# Files combined: 22
# File list:
#   allfiles.py
#   app.py
#   config/__init__.py
#   config/settings.py
#   db/__init__.py
#   db/database.py
#   db/setup.py
#   logging/__init__.py
#   logging/setup.py
#   models/__init__.py
#   models/book.py
#   repo/__init__.py
#   repo/books_repo.py
#   scraping/__init__.py
#   scraping/book_builder.py
#   scraping/fetch_catalogue.py
#   scraping/fetch_details.py
#   scraping/fetcher.py
#   scraping/parse.py
#   scraping/parse_primitives.py
#   scraping/urls.py
#   scraping/urls_detail_pages.py
================================================================================
