"""Module for describing PostgresSaver class."""
import logging
import os
from datetime import datetime

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch

import service_db


class PostgresSaver(object):
    """Class for loading data to PostgreSQL."""

    def __init__(
        self,
        conn: _connection,
        tables_settings: dict,
        schema_name: str,
    ):
        """Init the PostgresSaver object.

        Args:
            conn: connection to PostgresSQL database
            tables_settings: dictionary with table settings.
            schema_name: name of the database schema
        """
        self.connection = conn
        self.tables_settings = tables_settings
        self.schema_name = schema_name

    def delete_data_from_table(self, table_name):
        """Delete all the data from table_name.

        Args:
            table_name: name of the table in FROM clause
        """
        sql = service_db.create_delete_query(table_name, self.schema_name)
        with self.connection.cursor() as cur:
            try:
                cur.execute(sql)
            except Exception as err:
                logging.exception(
                    'Error occurred while deleting data from the tables: ' +
                    '{0}'.format(err),
                 )

    def delete_all_data(self):
        """Delete the data from all the tables."""
        # traverse the table in reverse order
        for table_name in list(self.tables_settings.keys())[::-1]:
            self.delete_data_from_table(table_name)

    def save_data_to_table(self, table_name, table_data):
        """Insert data to PostgreSQL table.

        Args:
            table_name: name of the table
            table_data: data, loaded from SQLite
        """
        table_settings = self.tables_settings.get(table_name)
        fields = table_settings['fields'] + table_settings['service_fields']
        insert_query = service_db.create_insert_query(
            table_name,
            self.schema_name,
            fields,
        )
        args_list = service_db.get_args_for_insert_query(
            table_name,
            table_data,
            table_settings,
        )
        with self.connection.cursor() as cur:
            try:
                execute_batch(
                     cur,
                     insert_query,
                     args_list,
                )
            except Exception as err:
                logging.exception(
                    'Error occurred while inserting data into ' +
                    '{0}: {1}'.format(table_name, err),
                )
