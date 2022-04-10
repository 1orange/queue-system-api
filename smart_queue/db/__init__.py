import os

import aiosql

sql = aiosql.from_path(
    os.path.abspath(
        os.path.join("smart_queue", "db", "queries", "queries.sql")
    ),
    driver_adapter="psycopg2",
)
