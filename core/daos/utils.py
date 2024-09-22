from typing import Union, Literal
from django.db import connection


def to_where(
    join: Union[Literal["AND"], Literal["OR"]] = "AND",
    prefix: bool = True,
    table_name: str = None,
    **kwargs,
):
    """
    Construct a where clause from the given arguments

    Args:
        join: Literal["AND", "OR"] - the join type
        prefix: bool - whether to prefix the where clause with WHERE
        table_name: str - the name of the table, or None if not applicable
        **kwargs: the arguments to construct the where clause from

    Returns:
        ret: str - the constructed where clause
    """
    ret = ""
    table_name = f" {table_name}." if table_name is not None else ""
    if not all(v is None for v in kwargs.values()):
        # need a where clause
        ret += " WHERE" if prefix else f" {join} "
        for k, v in kwargs.items():
            if v is not None:
                if isinstance(v, list):  # is an array, which means it must be for tags
                    ret += f" {table_name}{k} @> %s::tag_enum[] {join} "
                else:
                    ret += f" {table_name}{k} = %s {join} "
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
