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
