from logging import getLogger
from pathlib import Path
from urllib.parse import urljoin

logger = getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]

BASE_SITE = "https://books.toscrape.com/"
CATALOGUE_SITE = urljoin(BASE_SITE, "catalogue/")

# NUM_PAGES is hardcoded because there are fifty catalogue pages in books.toscrape.com
NUM_PAGES = 50

DATA_DIR = BASE_DIR / "data/"
DATA_DIR.mkdir(parents=True, exist_ok=True)

MAPPING_DIR = DATA_DIR / "mappings"
MAPPING_DIR.mkdir(parents=True, exist_ok=True)

CATALOGUE_MAPPING_FILE = MAPPING_DIR / "catalogue_mapping.json"

DETAILS_MAPPING_FILE = MAPPING_DIR / "details_mapping.json"

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
