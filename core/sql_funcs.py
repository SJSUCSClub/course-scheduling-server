import json
import datetime
from django.db import connection


''' A list of key value pairs for each item in a row and its corresponding column name'''


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def dictionify(data, rows, fetchall=True):

    if fetchall:
        json_data = []
        for result in data:
            json_data.append(dict(zip(rows, result)))
    else:
        json_data = dict(zip(rows, data))

    json_dump = json.dumps(json_data, default=default)
    return json.loads(json_dump)


def run_sql(query, col_tuples=None):
    with connection.cursor() as cursor:
        if col_tuples is not None:
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


def where(table, columns, resulting_cols=['*'], like=False, Or=False, orderby=False, orderby_col=None, page=None, limit=None, tags=None):
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

    if tags and len(tags) > 0:
        new_tags = []
        for tag in tags:
            new_tags.append("'" + tag + "'")
        tag_str = '(array[' + ','.join(new_tags) + '])::tag_enum[]'
        # col_tuple += ('"tags"', )
        col_list.append(tag_str + '<@tags')
    if Or:
        col_join = ' OR '.join(col_list)
    else:
        col_join = ' AND '.join(col_list)

    query += col_join

    if orderby and orderby_col is not None:
        query = orderby(query, orderby_col)

    if page:
        if limit is None or limit not in ['10', '20', '50']:
            limit = 10
        query += " LIMIT %s OFFSET %s"
        col_tuple += (limit, (int(page) - 1)*int(limit), )

    data, rows = run_sql(query, col_tuple)

    return dictionify(data, rows)


''' merge rows from different tables and return json object'''


def row_merge(objs):
    first = objs[0]

    for i in range(1, len(objs)):
        first = merge(first, objs[i])

    return first


def merge(json1, json2):
    for key in json2.keys():
        json1[key] = json2[key]

    return json1
    # with connection.cursor() as cursor:
    #     if id is not None:
    #         cursor.execute(
    #             "SELECT * FROM Schedules WHERE class_number=%s", [id])
    #         rows = [x[0] for x in cursor.description]
    #         schedules = cursor.fetchone()
    #         # print(schedules[14])

    #         ''' Querying for professors per schedule '''

    #         json_data = dict(zip(rows, schedules))

    #     else:
    #         cursor.execute("SELECT * FROM Schedules")
    #         rows = [x[0] for x in cursor.description]
    #         schedules = cursor.fetchall()
    #         json_data = []
    #         for result in schedules:
    #             # json_data = dict(zip(rows, all_courses))
    #             json_data.append(dict(zip(rows, result)))
    # print(json_data)

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM Courses")
    #     all_courses = cursor.fetchall()
    #     rows = [x[0] for x in cursor.description]

    # json_data = []
    # for result in all_courses:
    #     # json_data = dict(zip(rows, all_courses))
    #     json_data.append(dict(zip(rows, result)))

    # print(json_data[0])
