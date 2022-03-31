"""Main program, that loads data from sqlite to postgres."""
import logging
import os
import sqlite3
import service_db

from contextlib import contextmanager

import dotenv
import psycopg2
from psycopg2.extras import DictCursor

from postgres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader
from tables_settings import get_tables_settings


@contextmanager
def conn_context(db_path: str):
    """Yield the context manager for SQlite.

    Args:
        db_path: the path to sqlite database file

    Yields:
        connection: sqlite3.Connection
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite_to_postgres():
    """Load data from SQLite to Postgres."""

    dotenv.load_dotenv()
    dsl = {
        'dbname': os.environ.get('POSTGRES_DBNAME'),
        'user': os.environ.get('USER'),
        'password': os.environ.get('PASSWORD'),
        'host': os.environ.get('HOST'),
        'port': os.environ.get('PORT'),
        }
    sqlite_dbname = os.environ.get('SQLITE_DBNAME')
    with conn_context(sqlite_dbname) as sqlite_conn, \
         psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:

        tables_settings = get_tables_settings()
        page_size = int(os.environ.get('PAGE_SIZE'))

        postgres_saver = PostgresSaver(
            pg_conn,
            tables_settings,
            os.environ.get('POSTGRES_SCHEMA_NAME'),
        )
        sqlite_loader = SQLiteLoader(sqlite_conn, tables_settings)

        postgres_saver.delete_all_data()

        for table_name in list(tables_settings.keys()):
            table_settings = tables_settings[table_name]

            curs = sqlite_loader.get_cursor_for_select(table_name)

            while table_data := sqlite_loader.extract_data_from_cursor(
                curs,
                table_settings['dataclass'],
                page_size,
            ):
                postgres_saver.save_data_to_table(table_name, table_data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_from_sqlite_to_postgres()
    logging.info('OK')
