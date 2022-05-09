from asyncio.log import logger
from collections import namedtuple
from typing import List, NamedTuple, Optional

import pendulum
import psycopg2
from psycopg2.extras import NamedTupleCursor

from smart_queue import config
from smart_queue.db import sql
from smart_queue.db.helpers.autocommit import one_transaction_ctx


def evaluate_client_priority(time_arrived, burst_time, urgency) -> int:
    # NOTE: Evaluate alghoritm

    duration = pendulum.now() - time_arrived

    # # normalize elapsed_time
    # elapsed_time = duration.seconds

    return (duration.seconds * urgency) / burst_time


def reevaluate_queue():
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        with one_transaction_ctx(pg):
            try:
                evaluated_clients = [
                    {
                        "uuid": client.uuid,
                        "priority": evaluate_client_priority(
                            time_arrived=pendulum.instance(client.arrived),
                            burst_time=client.burst_time,
                            urgency=client.urgency
                        ),
                    }
                    for client in sql.get_queue_status(pg)
                ]

                sql.reevaluate_queue(pg, evaluated_clients)

            except Exception as e:
                logger.info(f"Unhandled exception:\r\n{e}")
                pg.rollback()

        return


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
        fetched_client = sql.get_current_client(pg)

        if fetched_client:
            current_client = namedtuple(
                "Client", ["uuid", "order_number", "arrived", "condition_name", "priority"]
            )

            return current_client(
                fetched_client.uuid,
                fetched_client.order_number,
                pendulum.instance(fetched_client.arrived).to_time_string(),
                fetched_client.condition_name,
                fetched_client.priority
            )


def insert_client(condition_id: int) -> NamedTuple:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        resp = sql.insert_client(pg, condition_id=condition_id)
        reevaluate_queue()

        return resp

def insert_condition(
    name: str, burst_time: int, desc: Optional[str] = None, urgency: int = 1
) -> None:
    # pylint: disable=E1101
    with psycopg2.connect(
        **config.database, cursor_factory=NamedTupleCursor
    ) as pg:
        sql.insert_condition(pg, name=name, desc=desc, burst_time=burst_time, urgency=urgency)


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
            "Client", ["uuid", "order_number", "arrived", "condition_name", "priority"]
        )

        clients = []

        for fetched_client in sql.get_queue_status(pg):
            clients.append(
                client(
                    fetched_client.uuid,
                    fetched_client.order_number,
                    pendulum.instance(fetched_client.arrived).to_time_string(),
                    fetched_client.condition_name,
                    fetched_client.priority
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
        reevaluate_queue()

        return
