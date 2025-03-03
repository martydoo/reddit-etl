import argparse
import logging

from db import db_factory

logger = logging.getLogger(__name__)


def construct():
    """Setup database schema."""
    db = db_factory("sqlite3", "reddit.db")
    with db.managed_cursor() as cur:
        logger.info("Creating posts table.")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                community TEXT,
                title TEXT,
                score INT,
                url TEXT,
                comments INT,
                created TEXT,
                text TEXT,
                modified DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ;
            """
        )


def teardown():
    """Drop database schema."""
    db = db_factory("sqlite3", "reddit.db")
    with db.managed_cursor() as cur:
        logger.info("Dropping posts table.")
        cur.execute(
            """
            DROP TABLE IF EXISTS
                posts
            ;
            """
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset-db", action="store_true", help="Reset database schema."
    )
    args = parser.parse_args()
    logging.basicConfig(filename="etl.log", level=logging.INFO)

    if args.reset_db:
        teardown()
        construct()
