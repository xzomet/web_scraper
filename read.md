---

# Book Scraper – books.toscrape.com

A Python-based web scraper that collects catalogue and detail information from
[https://books.toscrape.com](https://books.toscrape.com) and persists the data into a SQLite database.

The project is designed with a clear separation of concerns, deterministic scraping, and testable parsing logic.

---

## Features

* Deterministic URL → HTML file mapping
* Resume-safe scraping (HTML persisted to disk)
* Separate catalogue and detail scraping stages
* Structured parsing into domain models
* SQLite persistence with upsert semantics
* Configurable logging and retry logic
* Test coverage for parsing primitives and parsers

---

## Architecture Overview

The scraper is organized as a pipeline:

```
URLs → Fetching → HTML storage → Parsing → Domain models → Repository → Database
```

Key design goals:

* No network access during parsing
* No database access during parsing
* Idempotent scraping steps
* Clear boundaries between layers

---

## Project Structure

```
book_scraper/
├── app.py                 # Orchestration entry point
├── config/                # Global settings and constants
├── db/                    # SQLite setup and connection handling
├── log_config/            # Logging configuration
├── models/                # Domain models (Book)
├── repo/                  # Database access layer
└── scraping/
    ├── urls.py            # URL generation and mapping
    ├── fetcher.py         # HTTP fetching and persistence
    ├── parse.py           # High-level HTML parsing
    ├── parse_primitives.py# Low-level parsing helpers
    └── book_builder.py    # Book object construction
```

---

## Installation

This project uses **Poetry** for dependency management.

```bash
poetry install
```

---

## Usage

Run the full scraping pipeline:

```bash
python -m book_scraper.app
```

This will:

1. Create the database schema (if not present)
2. Generate catalogue URL mappings
3. Fetch catalogue HTML pages
4. Parse catalogue pages and persist books
5. (Optionally) fetch and parse detail pages
6. Upsert enriched book data into SQLite

HTML files and mapping files are stored under `data/`.

---

## Development

Run tests:

```bash
pytest
```

Code quality tools:

```bash
black .
ruff .
```

---

## Notes

* Parsing logic is intentionally strict and defensive.
* Missing fields are allowed at the domain level and resolved via upserts.
* Network failures do not corrupt state due to deterministic file storage.
* This project is intended as a learning and architecture-focused scraper, not a high-throughput crawler.

---

## License

MIT

---
