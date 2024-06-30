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
        
def run_change_sql(query,col_tuples=None):
    with connection.cursor() as cursor:
        if col_tuples is not None:
            cursor.execute(query, params=col_tuples)
        else:
            cursor.execute(query)
        rows_changed = cursor.rowcount
        return {"message": f"{rows_changed} row(s) were changed"}

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

# def addUser(email,name):
#     query = f'INSERT INTO Users (id,name,email,is_professor,username) VALUES({email[0:-9]},{name},{email},FALSE,generateUsername())'
#     return run_change_sql(query)

def calculate_votes(table,columns):
    col_tuple = tuple(columns.values())
    query = f"SELECT SUM(CASE WHEN vote = true THEN 1 ELSE 0 END) AS upvotes, SUM(CASE WHEN vote = false THEN 1 ELSE 0 END) AS downvotes FROM {table} WHERE user_id = %s AND review_id = %s"
    return run_sql(query,col_tuple)

def tags(value):
    value = value.replace("[","{").replace("]","}").replace("'","")
    return value

def insert(table, columns):
    select_cols = ','.join(columns.keys())
    placeholders = ','.join(['%s'] * len(columns))
    query = f'INSERT INTO {table}({select_cols}) VALUES ({placeholders})'
    if 'tags' in columns:
        columns["tags"] = tags(columns["tags"])
    col_tuple = tuple(columns.values())

    return run_change_sql(query,col_tuple)

def update(table,columns,where):
    col_tuple = tuple()
    if 'tags' in columns:
        columns["tags"] = tags(columns["tags"])
    keys = list(columns.keys())
    conditions = list(where)
    query = f'UPDATE {table} SET '
    for key in keys:
        query+= key + " = %s, "
        col_tuple+= (columns[key],)
    query = query.rstrip(", ")
    query += " WHERE "
    for condition in conditions:
        query+= condition + " = %s AND "
        col_tuple+=(where[condition],)
    query = query.rstrip("AND ")
    return run_change_sql(query,col_tuple)

def delete(table,columns):
    col_tuple = tuple()
    query = f'DELETE FROM {table} WHERE '
    keys = list(columns.keys())
    for key in keys:
        query+= key + " = %s AND "
        col_tuple+= (columns[key],)
    query = query.rstrip("AND ")
    return run_change_sql(query,col_tuple)