"""Check consistency of SQLite source and PostreSQL destination."""

import os
import sqlite3

import dotenv
import main
import psycopg2
import pytest
import service_db as service_db
import tables_settings as tables_settings
from psycopg2.extras import DictCursor

dotenv.load_dotenv()

tab_settings = tables_settings.get_tables_settings()

sqlite_conn = sqlite3.connect(os.environ.get('SQLITE_DBNAME'))
sqlite_conn.row_factory = sqlite3.Row

dsl = {
    'dbname': os.environ.get('POSTGRES_DBNAME'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWORD'),
    'host': os.environ.get('HOST'),
    'port': os.environ.get('PORT'),
}
postgres_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)

@pytest.mark.parametrize(
    'table_name',
    ['genre', 'person', 'film_work', 'genre_film_work', 'person_film_work'],
)
def test_check_count_rows(table_name):
    """Check that the row count between source and destinaion are equal.

    Args:
        table_name: name of the table being tested
    """
    sqlite_curs = sqlite_conn.cursor()
    sqlite_curs.execute('SELECT COUNT(*) FROM {0};'.format(table_name))
    sqlite_count = sqlite_curs.fetchone()[0]

    postgres_curs = postgres_conn.cursor()
    postgres_curs.execute(
        'SELECT COUNT(*) FROM content.{0};'.format(table_name),
    )
    postgres_count = postgres_curs.fetchone()[0]

    assert sqlite_count == postgres_count


@pytest.mark.parametrize(
    'table_name',
    ['genre', 'person', 'film_work', 'genre_film_work', 'person_film_work'],
)
def test_check_data_in_tables(table_name):
    """Test that data from SQLite and PostgreSQL are the same.

    Args:
        table_name: name of the table
    """
    fields = tab_settings[table_name]['fields']

    postgres_curs = postgres_conn.cursor()
    query = service_db.create_select_query(table_name, 'content', fields)
    postgres_curs.execute(query)

    got_data = False
    for postgres_row in postgres_curs:
        got_data = True
        id_value = dict(postgres_row)['id']
        query = service_db.create_select_query(table_name, '', fields, ['id'])
        sql_curs = sqlite_conn.cursor()
        sql_curs.execute(query, (id_value,))
        sqlite_row = dict(sql_curs.fetchone())

        for field in fields:
            assert postgres_row[field] == sqlite_row[field]

    assert got_data

def setup_module():
    main.load_from_sqlite_to_postgres()