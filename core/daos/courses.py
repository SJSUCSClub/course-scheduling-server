from django.db import connection
from .utils import to_where
from core.models import Courses


def course_select_summary(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT * from courses where department=%s and course_number=%s"
        cursor.execute(query, (dept, course_number))
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))


def course_select_paginated_reviews(dept, course_number, limit, page, tags=[]):
    with connection.cursor() as cursor:
        query = """
            SELECT r.*, u.name AS reviewer_name, u.username AS reviewer_username, p.id AS professor_id, p.name AS professor_name, p.email AS professor_email
            FROM reviews r
            LEFT JOIN users u ON r.user_id = u.id
            INNER JOIN users p ON r.user_id = p.id
            WHERE r.department=%s AND course_num=%s AND r.tags @> %s::tag_enum[]
            LIMIT %s
            OFFSET %s;
        """
        cursor.execute(query, (dept, course_number, tags, limit, (page - 1) * limit))
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))


# STATS
def course_select_average_grade(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT get_course_average_grade(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()[0]


def course_select_average_quality(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT get_course_average_quality(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()[0]


def course_select_average_ease(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT get_course_average_ease(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()[0]


def course_select_take_again_percent(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT get_course_take_again_percent(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()[0]


def course_select_total_reviews(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT get_course_total_reviews(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()[0]


def course_select_average_rating(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT get_course_average_rating(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()[0]


def course_select_ease_distribution(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT * from get_course_ease_distribution(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()


def course_select_grade_distribution(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT * from get_course_grade_distribution(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()


def course_select_quality_distribution(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT * from get_course_quality_distribution(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()


def course_select_rating_distribution(dept, course_number):
    with connection.cursor() as cursor:
        query = "SELECT * from get_course_rating_distribution(%s, %s)"
        cursor.execute(query, (dept, course_number))
        return cursor.fetchone()


def course_search_by_filters(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    limit: int = None,
    page: int = None,
):
    """
    Select courses from the database with any of the given filters

    Args:
        department: string - the department of the course
        course_number: string - the number of the course
        professor_id: string - the id of the professor
        tags: List[str] - the tags of the course
        limit: int - the number of results to return per page; only effective if page is also provided
        page: int - the 1-indexed page number; only effective if limit is also provided

    Returns:
        out: List[dict] - A list of courses
    """
    args = locals()
    page = args.pop("page")
    limit = args.pop("limit")
    query = "SELECT * FROM courses" + to_where(**args)

    if page and limit:
        query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    with connection.cursor() as cursor:
        cursor.execute(query, list(filter(lambda x: x is not None, args.values())))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def course_search_by_filters_count(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
) -> int:
    """
    Returns the number of courses that match the given filters

    Args:
        department: string - the department of the course
        course_number: string - the number of the course
        professor_id: string - the id of the professor
        tags: List[str] - the tags of the course

    Returns:
        out: int - The total number of courses matching the given filters
    """
    args = locals()
    query = "SELECT COUNT(*) FROM courses" + to_where(**args)

    with connection.cursor() as cursor:
        cursor.execute(query, list(filter(lambda x: x is not None, args.values())))
        return cursor.fetchone()[0]


def course_search_by_filters_departments(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
):
    args = locals()
    query = (
        "SELECT department, COUNT(*) as count FROM (SELECT * FROM COURSES"
        + to_where(**args)
        + ") GROUP BY department"
    )

    with connection.cursor() as cursor:
        cursor.execute(query, list(filter(lambda x: x is not None, args.values())))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def course_search_by_similarity(
    query: str,
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    limit: int = None,
    page: int = None,
):
    """
    Search for courses by similarity to the given query,
    applying all the given filters
    """
    args = locals()
    page = args.pop("page")
    limit = args.pop("limit")
    query = args.pop("query")
    sql_query1 = (
        "SELECT *, similarity((department || ' ' || course_number), %s) AS similarity FROM courses"
        + to_where(**args)
    )
    sql_query2 = "SELECT *, similarity(name, %s) AS similarity FROM courses" + to_where(
        **args
    )
    fields = ", ".join([field.name for field in Courses._meta.fields])
    # TODO - make similarity threshold configurable
    full_query = f"""
        SELECT {fields} FROM 
        ({sql_query1} UNION {sql_query2})
        WHERE similarity > 0.4
        GROUP BY {fields} 
        ORDER BY MAX(similarity) DESC
    """

    if page and limit:
        full_query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    with connection.cursor() as cursor:
        cursor.execute(
            full_query,
            [query, *list(filter(lambda x: x is not None, args.values()))] * 2,
        )
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def course_search_by_similarity_count(
    query: str,
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
):
    """
    Search for courses by similarity to the given query,
    applying all the given filters
    """
    args = locals()
    query = args.pop("query")
    sql_query1 = (
        "SELECT *, similarity((department || ' ' || course_number), %s) AS similarity FROM courses"
        + to_where(**args)
    )
    sql_query2 = "SELECT *, similarity(name, %s) AS similarity FROM courses" + to_where(
        **args
    )
    fields = ", ".join([field.name for field in Courses._meta.fields])
    full_query = f"""
        SELECT COUNT(*) FROM
        (SELECT {fields} FROM 
        ({sql_query1} UNION {sql_query2})
        WHERE similarity > 0.4
        GROUP BY {fields})
    """

    with connection.cursor() as cursor:
        cursor.execute(
            full_query,
            [query, *list(filter(lambda x: x is not None, args.values()))] * 2,
        )
        return cursor.fetchone()[0]


def course_search_by_similarity_departments(
    query: str,
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
):
    """
    Search for courses by similarity to the given query,
    applying all the given filters
    """
    args = locals()
    query = args.pop("query")
    sql_query1 = (
        "SELECT *, similarity((department || ' ' || course_number), %s) AS similarity FROM courses"
        + to_where(**args)
    )
    sql_query2 = "SELECT *, similarity(name, %s) AS similarity FROM courses" + to_where(
        **args
    )
    fields = ", ".join([field.name for field in Courses._meta.fields])
    full_query = f"""
        SELECT department, COUNT(*) as count FROM
        (SELECT {fields} FROM 
        ({sql_query1} UNION {sql_query2})
        WHERE similarity > 0.4)
        GROUP BY department
    """

    with connection.cursor() as cursor:
        cursor.execute(
            full_query,
            [query, *list(filter(lambda x: x is not None, args.values()))] * 2,
        )
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
