import logging
from contextlib import contextmanager

import psycopg2

logger = logging.getLogger(__name__)


@contextmanager
def one_transaction_ctx(connection, autocommit=False):
    if connection.autocommit == autocommit:
        with connection:
            yield connection
        return

    try:
        try:
            connection.autocommit = autocommit
        except psycopg2.Error as e:
            logger.error(f"Failed to change autocommit: {e}")
            raise

        with connection:
            yield connection

    finally:
        connection.autocommit = not autocommit
