-- name: initialize_db#
CREATE SCHEMA IF NOT EXISTS sq;

CREATE SEQUENCE sq.order_number_seq
MINVALUE 1
INCREMENT 1
START 1;

CREATE TABLE IF NOT EXISTS sq.conditions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    -- complexity NOTE: TIME COMPLEXITY OF act

    UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS sq.queue(
    uuid text PRIMARY KEY DEFAULT md5(random()::text || clock_timestamp()::text)::uuid,
    order_number INTEGER NOT NULL DEFAULT nextval('sq.order_number_seq'),
    arrived TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    condition_id INTEGER REFERENCES sq.conditions (id),
    checked boolean NOT NULL DEFAULT FALSE,
    priority INTEGER DEFAULT 1
);

ALTER SEQUENCE sq.order_number_seq
OWNED BY sq.queue.order_number;