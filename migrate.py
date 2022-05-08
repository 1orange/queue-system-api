import logging
import logging.config
import os

import aiosql
import psycopg2
from psycopg2.extras import NamedTupleCursor

from smart_queue import config

logger = logging.getLogger(__name__)


def load_db_schema():
    return aiosql.from_path(
        os.path.abspath(
            os.path.join("smart_queue", "db", "queries", "schema.sql")
        ),
        driver_adapter="psycopg2",
    )


def migrate_db(sql):
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        logger.info("Migrating DB!")
        sql.initialize_db(pg)
        logger.info("Done!")


if __name__ == "__main__":
    db_schema = load_db_schema()

    logging.config.dictConfig(config.logging)

    migrate_db(db_schema)
