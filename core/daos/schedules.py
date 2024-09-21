from core.daos.utils import to_where, fetchone, fetchall


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

    return fetchall(query, *list(filter(lambda x: x is not None, args.values())))


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

    return fetchone(query, *list(filter(lambda x: x is not None, args.values())))[0]


def schedule_search_by_filters(
    term: str = None,
    year: str = None,
    course_number: str = None,
    department: str = None,
    mode_of_instruction: str = None,
    units: str = None,
    professor_name: str = None,
    page: int = None,
    limit: int = None,
):
    args = locals()
    page = args.pop("page")
    limit = args.pop("limit")
    schedule_filters = {
        key: val for key, val in args.items() if key != "professor_name"
    }
    professor_filters = {"name": professor_name}
    query = f"""
        SELECT s.*, c.name AS course_title, u.name AS professor_name FROM schedules s
        LEFT JOIN courses c ON s.department = c.department AND s.course_number = c.course_number
        LEFT JOIN users u ON s.professor_id = u.id
        {to_where(**schedule_filters, prefix=True, table_name="s")}
        {to_where(**professor_filters, prefix=not any(schedule_filters.values()), table_name="u")}
    """

    if page and limit:
        query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    return fetchall(query, *list(filter(lambda x: x is not None, args.values())))


def schedule_search_by_filters_count(
    term: str = None,
    year: str = None,
    course_number: str = None,
    department: str = None,
    mode_of_instruction: str = None,
    units: str = None,
    professor_name: str = None,
    count_by: str = None,
):
    args = locals()
    count_by = args.pop("count_by")
    schedule_filters = {
        key: val for key, val in args.items() if key != "professor_name"
    }
    professor_filters = {"name": professor_name}
    count_query = "COUNT(*) as count"
    group_by = ""
    if count_by:
        if count_by == "professor_name":
            count_query = f"u.name as professor_name, COUNT(*) as count"
            group_by = f"GROUP BY u.name"
        else:
            count_query = f"s.{count_by}, COUNT(*) as count"
            group_by = f"GROUP BY s.{count_by}"
    query = f"""
        SELECT {count_query} FROM schedules s
        LEFT JOIN courses c ON s.department = c.department AND s.course_number = c.course_number
        LEFT JOIN users u ON s.professor_id = u.id
        {to_where(**schedule_filters, prefix=True, table_name="s")}
        {to_where(**professor_filters, prefix=not any(schedule_filters.values()), table_name="u")}
        {group_by}
    """

    return fetchall(query, *list(filter(lambda x: x is not None, args.values())))


def schedule_search_by_similarity(
    query: str,
    term: str = None,
    year: str = None,
    professor_name: str = None,
    course_number: str = None,
    department: str = None,
    mode_of_instruction: str = None,
    units: str = None,
    page: int = None,
    limit: int = None,
):
    args = locals()
    page = args.pop("page")
    limit = args.pop("limit")
    query = args.pop("query")
    schedule_filters = {
        key: val for key, val in args.items() if key != "professor_name"
    }
    professor_filters = {"name": professor_name}
    sql_query = f"""
        SELECT s.*, c.name AS course_title, u.name AS professor_name, similarity(c.name, %s) AS similarity FROM schedules s
        LEFT JOIN courses c ON s.department = c.department AND s.course_number = c.course_number
        LEFT JOIN users u ON s.professor_id = u.id
        WHERE similarity > 0.4
        {to_where(**schedule_filters, prefix=False, table_name="s")}
        {to_where(**professor_filters, prefix=False, table_name="u")}
        ORDER BY similarity DESC
    """

    if page and limit:
        sql_query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    return fetchall(
        sql_query, query, *list(filter(lambda x: x is not None, args.values()))
    )


def schedule_search_by_similarity_count(
    query: str,
    term: str = None,
    year: str = None,
    professor_name: str = None,
    course_number: str = None,
    department: str = None,
    mode_of_instruction: str = None,
    units: str = None,
    count_by: str = None,
):
    """
    Count the number of schedules that match the query with any of the given filters,
    or return the count of all the schedules that have a certain filter applied

    Args:
        query: string - the query to search for
        term: string - the term of the schedule
        year: string - the year of the schedule
        professor_name: string - the name of the professor
        course_number: string - the number of the course
        department: string - the department of the course
        mode_of_instruction: string - the mode of instruction of the course
        units: string - the units of the course
        count_by: string - the column to count by, or None to count all

    Returns:
        out: List[dict] - The number of schedules that match the query
    """
    args = locals()
    count_by = args.pop("count_by")
    query = args.pop("query")
    schedule_filters = {
        key: val for key, val in args.items() if key != "professor_name"
    }
    professor_filters = {"name": professor_name}
    count_query = "COUNT(*) as count"
    group_by = ""
    if count_by is not None:
        if count_by == "professor_name":
            count_query = f"u.name as professor_name, COUNT(*) as count"
            group_by = f" GROUP BY u.name"
        else:
            count_query = f"s.{count_by}, COUNT(*) as count"
            group_by = f" GROUP BY s.{count_by}"
    sql_query = f"""
        SELECT {count_query} FROM schedules s
        LEFT JOIN courses c ON s.department = c.department AND s.course_number = c.course_number
        LEFT JOIN users u ON s.professor_id = u.id
        WHERE similarity(c.name, %s) > 0.4
        {to_where(**schedule_filters, prefix=False, table_name="s")}
        {to_where(**professor_filters, prefix=False, table_name="u")}
        {group_by}
    """

    return fetchall(
        sql_query, query, *list(filter(lambda x: x is not None, args.values()))
    )
