from tokenize import Name
from typing import List, NamedTuple, Optional
import pendulum

import psycopg2
from collections import namedtuple
from psycopg2.extras import NamedTupleCursor

from smart_queue import config
from smart_queue.db import sql


def check_client_status(uuid) -> str:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        if sql.find_client_by_id(pg, uuid=uuid).count < 1:
            return "SERVED"

        if sql.get_current_client(pg).uuid == uuid:
            return "INSIDE"

        return "WAITING"


def get_current_client() -> NamedTuple:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        fetched_client =  sql.get_current_client(pg)

        if fetched_client:
            current_client = namedtuple(
                'Client',
                ['uuid', 'order_number', 'arrived', 'condition_name']
            )

            return current_client(
                fetched_client.uuid,
                fetched_client.order_number,
                pendulum.instance(fetched_client.arrived).to_time_string(),
                fetched_client.condition_name
            )


def insert_client(condition_id: int) -> NamedTuple:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        return sql.insert_client(pg, condition_id=condition_id)


def insert_condition(
    name: str, complexity: int, desc: Optional[str] = None
) -> None:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        sql.insert_condition(pg, name=name, desc=desc, complexity=complexity)


def delete_condition(id) -> None:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        sql.delete_condition(pg, id=id)


def get_queue_status() -> NamedTuple:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        client = namedtuple(
            'Client',
            ['uuid', 'order_number', 'arrived', 'condition_name']
        )

        clients = []


        for fetched_client in sql.get_queue_status(pg):
            clients.append(
                client(
                    fetched_client.uuid,
                    fetched_client.order_number,
                    pendulum.instance(fetched_client.arrived).to_time_string(),
                    fetched_client.condition_name
                )
            )

        return clients


def get_all_conditions() -> NamedTuple:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        return sql.get_all_conditions(pg)


def next_patient():
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        sql.delete_current_client(pg)

        return
    