from collections import namedtuple

from django.db import connection


def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_custom_sql_results(query: str, params: tuple):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return namedtuplefetchall(cursor)
