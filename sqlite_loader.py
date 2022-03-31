"""Declare SQLiteLoader for loading data in SQLite database."""
import dataclasses
import logging
import sqlite3

import service_db


class SQLiteLoader(object):
    """Load data from SQLite database."""

    def __init__(
            self,
            connection: sqlite3.Connection,
            table_settings: dict,
    ):
        """Init SQLiteLoader object.

        Args:
            connection: connection to SQLite database
            table_settings: info about columns of the tables etc.
        """
        self.connection = connection
        self.table_settings = table_settings

    @staticmethod
    def extract_data_from_cursor(
            cursor: sqlite3.Cursor,
            dataclass: dataclasses,
            size: int,
    ) -> []:
        """Extract data from cursor.

        Args:
            cursor: cursor for fetching sqlite data
            dataclass: class for creating objects, representing extracted data
            size: number of rows being read with each iteration

        Returns:
            the list of dataclass objects
        """
        records = cursor.fetchmany(size=size)
        data_list = []
        for row in records:
            row_source = dict(row)
            db_object = dataclass(**row_source)
            data_list.append(db_object)
        return data_list

    def get_cursor_for_select(
            self,
            table_name: str,
    ) -> []:
        """Convert the data from the table to the list of dataclass objects.

        Args:
            table_name (str): the name of the table we get data from.

        Returns:
            cursor for fetching data
        """
        table_settings = self.table_settings.get(table_name)

        curs = self.connection.cursor()
        sql = service_db.create_select_query(
            table_name,
            '',
            table_settings['fields'],
        )

        try:
            curs.execute(sql)
        except Exception as err:
            logging.exception(
                ('Error occurred while saving data from ' +
                 '{0}: {1}'.format(table_name, err)
                 ),
            )
            return None

        return curs

    def load_data(self) -> dict:
        """Save data from SQLite database to a dictionary.

        Returns:
            dict - dictionary with data from db, where the key is
            the name of the table
        """
        pass
        # genre_data = self.get_data_from_table('genre')
        # person_data = self.get_data_from_table('person')
        # film_work_data = self.get_data_from_table('film_work')
        # genre_film_work_data = self.get_data_from_table('genre_film_work')
        # person_film_work_data = self.get_data_from_table('person_film_work')
        #
        # return {
        #     'genre': genre_data,
        #     'person': person_data,
        #     'film_work': film_work_data,
        #     'genre_film_work': genre_film_work_data,
        #     'person_film_work': person_film_work_data,
        # }
