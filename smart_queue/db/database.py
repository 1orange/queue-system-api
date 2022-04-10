from tokenize import Name
from typing import List, NamedTuple

import psycopg2
from psycopg2.extras import NamedTupleCursor

from smart_queue import config
from smart_queue.db import sql


def get_current_client() -> NamedTuple:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        return sql.get_current_client(pg)


def insert_client(condition_id: int) -> NamedTuple:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        return sql.insert_client(pg, condition_id=condition_id)


def get_queue_status() -> NamedTuple:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        return sql.get_queue_status(pg)
