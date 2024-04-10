import json
from django.db import connection


''' A list of key value pairs for each item in a row and its corresponding column name'''


def dictionify(data, rows, fetchall=True):

    if fetchall:
        json_data = []
        for result in data:
            json_data.append(dict(zip(rows, result)))
    else:
        json_data = dict(zip(rows, data))

    return json_data


def run_sql(query, col_tuples=None):
    with connection.cursor() as cursor:
        if col_tuples is not None:
            # print(query, col_tuples)
            print(type(col_tuples))
            cursor.execute(query, params=col_tuples)
        else:
            cursor.execute(query)
        data = cursor.fetchall()
        rows = [x[0] for x in cursor.description]

    return data, rows


''' For all "Select *" queries '''


def general_statements(table, resulting_cols=['*'], orderby=False, orderby_col=None):

    select_cols = ','.join(resulting_cols)
    query = f'SELECT {select_cols} FROM {table}'
    if orderby and orderby_col is not None:
        query = orderby(query, orderby_col)

    data, rows = run_sql(query)

    return dictionify(data, rows)

# Order by specific column


def orderby(query, orderby_col):
    return query + f' ORDER BY {orderby_col}'


'''Where statements'''


def where(table, columns, resulting_cols=['*'], like=False, Or=False, orderby=False, orderby_col=None):
    select_cols = ','.join(resulting_cols)
    query = f'SELECT {select_cols} FROM {table} WHERE'
    col_list = []
    col_tuple = tuple()
    if like:
        for name, val in columns.items():
            col_tuple += (val,)
            col_list.append(" " + name + " LIKE '%$%s%'")

    else:
        for name, val in columns.items():
            col_tuple += (val,)
            col_list.append(' ' + name + '=%s')
    if Or:
        col_join = ' OR '.join(col_list)
    else:
        col_join = ' AND '.join(col_list)

    query += col_join

    if orderby and orderby_col is not None:
        query = orderby(query, orderby_col)

    data, rows = run_sql(query, col_tuple)
    return dictionify(data, rows)


''' merge rows from different tables and return json object'''


def row_merge(objs):
    first = objs[0]

    for i in range(1, len(objs)):
        first = first.extend(objs[i])

    return json.dumps(first)
