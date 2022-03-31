"""Contain settings for the tables."""
from models import Genre, Person, FilmWork, \
    PersonFilmWork, GenreFilmWork


def get_tables_settings() -> dict:
    """Create settings for the table.

    Returns:
        dict - table of settings.
    """
    tables_settings = {}

    # GENRE
    tables_settings['genre'] = {
        'dataclass': Genre,
        'fields': ['id', 'name', 'description'],
        'service_fields': ['created', 'modified'],
    }

    # PERSON
    tables_settings['person'] = {
        'dataclass': Person,
        'fields': ['id', 'full_name'],
        'service_fields': ['created', 'modified'],
    }

    # FILM_WORK
    tables_settings['film_work'] = {
        'dataclass': FilmWork,
        'fields': [
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
        ],
        'service_fields': ['created', 'modified'],
    }

    # GENRE_FILM_WORK
    tables_settings['genre_film_work'] = {
        'dataclass': GenreFilmWork,
        'fields': ['id', 'genre_id', 'film_work_id'],
        'service_fields': ['created'],
    }

    # PERSON_FILM_WORK
    tables_settings['person_film_work'] = {
        'dataclass': PersonFilmWork,
        'fields': ['id', 'person_id', 'film_work_id', 'role'],
        'service_fields': ['created'],
    }

    return tables_settings
