"""Module with service functions for working with database."""

from datetime import datetime


def table_with_schema(table_name, schema_name):
    """Get table with schema.

    Args:
        table_name: name of the table
        schema_name: name of the scheme
    """
    if schema_name:
        return '{0}.{1}'.format(schema_name, table_name)
    else:
        return table_name


def create_select_query(
        table_name: str,
        schema_name: str,
        fields: [],
        where_fields: [] = None,
) -> str:
    """Create SELECT query.

    Args:
        table_name: the table name in FROM clause
        schema_name: the schema name
        fields: list of the fields in SELECT case
        where_fields: list of the fields in WHERE case

    Returns:
        the string with SELECT query
    """

    query = 'SELECT '
    query += ','.join(fields)
    query += ' FROM {0}'.format(table_with_schema(table_name, schema_name))

    where_clause = ''
    if where_fields:
        index = 0
        where_clause = ' WHERE '
        for field in where_fields:
            where_clause += '{0} = ? and '.format(field)
            index += 1
        where_clause = where_clause[:-5]

    query += '{0};'.format(where_clause)

    return query


def create_insert_query(
        table_name: str,
        schema_name: str,
        fields: [],
) -> str:
    """Create INSERT query.

    Args:
        table_name: the table name in FROM clause
        schema_name: the schema name
        fields: list of the fields in SELECT case

    Returns:
        the string with INSERT query
    """
    fields_string = ', '.join(fields)
    values_string = ('%s, ' * len(fields))[:-2]
    return ('INSERT INTO {0} ({1}) VALUES({2});'.format(
        table_with_schema(table_name, schema_name),
        fields_string,
        values_string,
    )
    )


def create_delete_query(
        table_name: str,
        schema_name: str,
) -> str:
    """Create DELETE query.

    Args:
        table_name: the table name in FROM clause
        schema_name: the schema name

    Returns:
        the string with DELETE query
    """
    return 'DELETE FROM {0};'.format(
        table_with_schema(table_name, schema_name)
    )


def get_args_for_insert_query(
        table_name,
        table_data,
        table_settings,
) -> list:
    """Get list of arguments for insert query.

    Args:
        table_name: the name of the table
        table_data: the data from SQLite_Loader()
        table_settings: settings for the table

    Returns:
        the list of tuples of arguments for the INSERT query
    """
    arg_list = []
    for dc_object in table_data:
        args = []
        for field in table_settings['fields']:
            args.append(dc_object.__dict__[field])
        for _ in table_settings['service_fields']:
            args.append(datetime.now())
        arg_list.append(args)
    return arg_list
