from .utils import to_where, fetchone_as_dict, fetchone, fetchall
from core.models import Courses


def course_select_summary(dept, course_number):
    query = "SELECT * from courses where department=%s and course_number=%s"
    return fetchone_as_dict(query, dept, course_number)


def course_select_paginated_reviews(dept, course_number, limit, page, tags=[]):
    query = """
        SELECT r.*, u.name AS reviewer_name, u.username AS reviewer_username, p.id AS professor_id, p.name AS professor_name, p.email AS professor_email
        FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id
        INNER JOIN users p ON r.user_id = p.id
        WHERE r.department=%s AND course_num=%s AND r.tags @> %s::tag_enum[]
        LIMIT %s
        OFFSET %s;
    """
    return fetchone_as_dict(query, dept, course_number, tags, limit, (page - 1) * limit)


# STATS
def course_select_average_grade(dept, course_number):
    query = "SELECT get_course_average_grade(%s, %s)"
    return fetchone(query, dept, course_number)[0]


def course_select_average_quality(dept, course_number):
    query = "SELECT get_course_average_quality(%s, %s)"
    return fetchone(query, dept, course_number)[0]


def course_select_average_ease(dept, course_number):
    query = "SELECT get_course_average_ease(%s, %s)"
    return fetchone(query, dept, course_number)[0]


def course_select_take_again_percent(dept, course_number):
    query = "SELECT get_course_take_again_percent(%s, %s)"
    return fetchone(query, dept, course_number)[0]


def course_select_total_reviews(dept, course_number):
    query = "SELECT get_course_total_reviews(%s, %s)"
    return fetchone(query, dept, course_number)[0]


def course_select_average_rating(dept, course_number):
    query = "SELECT get_course_average_rating(%s, %s)"
    return fetchone(query, dept, course_number)[0]


def course_select_ease_distribution(dept, course_number):
    query = "SELECT * from get_course_ease_distribution(%s, %s)"
    return fetchone(query, dept, course_number)


def course_select_grade_distribution(dept, course_number):
    query = "SELECT * from get_course_grade_distribution(%s, %s)"
    return fetchone(query, dept, course_number)


def course_select_quality_distribution(dept, course_number):
    query = "SELECT * from get_course_quality_distribution(%s, %s)"
    return fetchone(query, dept, course_number)


def course_select_rating_distribution(dept, course_number):
    query = "SELECT * from get_course_rating_distribution(%s, %s)"
    return fetchone(query, dept, course_number)


def course_search_by_filters(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    units: str = None,
    satisfies_area: str = None,
    limit: int = None,
    page: int = None,
):
    """
    Select courses from the database with any of the given filters

    Args:
        department: string - the department of the course
        course_number: string - the number of the course
        professor_id: string - the id of the professor
        units: string - the units of the course
        satisfies_area: string - the area the course satisfies
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

    return fetchall(query, *list(filter(lambda x: x is not None, args.values())))


def course_search_by_filters_count(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    units: str = None,
    satisfies_area: str = None,
    count_by: str = None,
) -> int:
    """
    Returns the number of courses that match the given filters

    Args:
        department: string - the department of the course
        course_number: string - the number of the course
        professor_id: string - the id of the professor
        units: string - the units of the course
        satisfies_area: string - the area the course satisfies
        count_by: string - the column to count by, or None to count all

    Returns:
        out: int - The total number of courses matching the given filters
    """
    args = locals()
    count_by = args.pop("count_by")
    count_query = "COUNT(*) as count"
    group_by = ""
    not_null_clause = ""
    if count_by is not None:
        count_query = f"{count_by}, COUNT(*) as count"
        group_by = f"GROUP BY {count_by}"
        if not all(lambda x: x is None, args.values()):
            not_null_clause = f" AND {count_by} IS NOT NULL"
        else:
            not_null_clause = f" WHERE {count_by} IS NOT NULL"
    query = f"SELECT {count_query} FROM courses {to_where(**args)} {not_null_clause} {group_by}"
    return fetchall(query, *list(filter(lambda x: x is not None, args.values())))


def course_search_by_similarity(
    query: str,
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    units: str = None,
    satisfies_area: str = None,
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

    return fetchall(
        full_query,
        *([query, *list(filter(lambda x: x is not None, args.values()))] * 2),
    )


def course_search_by_similarity_count(
    query: str,
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    units: str = None,
    satisfies_area: str = None,
    count_by: str = None,
):
    """
    Search for courses by similarity to the given query,
    applying all the given filters
    """
    args = locals()
    query = args.pop("query")
    count_by = args.pop("count_by")
    sql_query1 = (
        "SELECT *, similarity((department || ' ' || course_number), %s) AS similarity FROM courses"
        + to_where(**args)
    )
    sql_query2 = "SELECT *, similarity(name, %s) AS similarity FROM courses" + to_where(
        **args
    )
    fields = ", ".join([field.name for field in Courses._meta.fields])
    count_query = "COUNT(*)"
    group_by = ""
    not_null_clause = ""
    if count_by is not None:
        count_query = f"{count_by}, COUNT(*) as count"
        group_by = f"GROUP BY {count_by}"
        not_null_clause = f" AND {count_by} IS NOT NULL"
    full_query = f"""
        SELECT {count_query} FROM
        (SELECT {fields} FROM 
        ({sql_query1} UNION {sql_query2})
        WHERE similarity > 0.4 {not_null_clause}
        GROUP BY {fields})
        {group_by}
    """

    return fetchall(
        full_query,
        *([query, *list(filter(lambda x: x is not None, args.values()))] * 2),
    )
