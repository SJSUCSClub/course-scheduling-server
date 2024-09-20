from typing import Union, Literal
from django.db import connection


def to_where(join: Union[Literal["AND"], Literal["OR"]] = "AND", **kwargs):
    ret = ""
    if not all(v is None for v in kwargs.values()):
        # need a where clause
        ret += " WHERE"
        for k, v in kwargs.items():
            if v is not None:
                if isinstance(v, list):  # is an array, which means it must be for tags
                    ret += f" {k} @> %s::tag_enum[] {join} "
                else:
                    ret += f" {k} = %s {join} "
        ret = ret.removesuffix(f" {join} ")
    return ret


def fetchall(query: str, *args):
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetchone(query: str, *args):
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        return cursor.fetchone()


def fetchone_as_dict(query: str, *args):
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))
