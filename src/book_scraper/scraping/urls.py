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
