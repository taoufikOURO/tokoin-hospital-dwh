"""Module for managing PostgreSQL connections."""

import psycopg2
from config.config import PG_CONFIG


def get_pg_connection():
    """Establishes a connection to the PostgreSQL database and returns the connection object."""
    return psycopg2.connect(**PG_CONFIG)
