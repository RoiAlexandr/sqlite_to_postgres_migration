import datetime
import uuid

from dataclasses import dataclass


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str


@dataclass
class Person:
    id: uuid.UUID
    full_name: str


@dataclass
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date
    rating: float
    type: str


@dataclass
class GenreFilmWork:
    id: uuid.UUID
    genre_id: uuid.UUID
    film_work_id: uuid.UUID


@dataclass
class PersonFilmWork:
    id: uuid.UUID
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
