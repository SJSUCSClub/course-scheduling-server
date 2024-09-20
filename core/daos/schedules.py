from django.db import connection
from core.daos.utils import to_where


def schedule_select(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    satisfies_area: str = None,
    limit: int = None,
    page: int = None,
):
    """
    Select schedules from the database with any of the given filters

    Args:
        department: string - the department of the course
        course_number: string - the number of the course
        professor_id: string - the id of the professor
        satisfies_area: string - the area the course satisfies
        limit: int - the number of results to return per page; only effective if page is also provided
        page: int - the 1-indexed page number; only effective if limit is also provided

    Returns:
        out: List[dict] - A list of schedules
    """
    args = locals()
    page = args.pop("page")
    limit = args.pop("limit")
    query = "SELECT * FROM schedules" + to_where(**args)

    if page and limit:
        query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"
    query += ";"

    with connection.cursor() as cursor:
        cursor.execute(query, list(filter(lambda x: x is not None, args.values())))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, el)) for el in cursor.fetchall()]


def schedule_select_counts(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    satisfies_area: str = None,
) -> int:
    """
    Select the total number of schedules from the database with any of the given filters

    Args:
        department: string - the department of the course
        course_number: string - the number of the course
        professor_id: string - the id of the professor
        satisfies_area: string - the area the course satisfies

    Returns:
        out: int - The total number of schedules
    """
    args = locals()
    query = "SELECT COUNT(*) FROM schedules" + to_where(**args)

    with connection.cursor() as cursor:
        cursor.execute(query, list(filter(lambda x: x is not None, args.values())))
        return cursor.fetchone()[0]
