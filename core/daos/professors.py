from .utils import fetchone, fetchone_as_dict, fetchall, insert


# SUMMARY
def professor_select_summary(professor_id):
    query = "SELECT id, name, email FROM users WHERE id = %s"
    return fetchone_as_dict(query, professor_id)


def professor_insert_view(professor_id):
    insert("professor_visits", {"professor_id": professor_id})


# STATS
def professor_select_average_grade(professor_id):
    query = "SELECT get_professor_average_grade(%s)"
    return fetchone(query, professor_id)[0]


def professor_select_average_quality(professor_id):
    query = "SELECT get_professor_average_quality(%s)"
    return fetchone(query, professor_id)[0]


def professor_select_average_ease(professor_id):
    query = "SELECT get_professor_average_ease(%s)"
    return fetchone(query, professor_id)[0]


def professor_select_take_again_percent(professor_id):
    query = "SELECT get_professor_take_again_percent(%s)"
    return fetchone(query, professor_id)[0]


def professor_select_total_reviews(professor_id):
    query = "SELECT get_professor_total_reviews(%s)"
    return fetchone(query, professor_id)[0]


def professor_select_average_rating(professor_id):
    query = "SELECT get_professor_average_rating(%s)"
    return fetchone(query, professor_id)[0]


def professor_select_ease_distribution(professor_id):
    query = "SELECT * from get_professor_ease_distribution(%s)"
    return fetchone(query, professor_id)


def professor_select_grade_distribution(professor_id):
    query = "SELECT * from get_professor_grade_distribution(%s)"
    return fetchone(query, professor_id)


def professor_select_quality_distribution(professor_id):
    query = "SELECT * from get_professor_quality_distribution(%s)"
    return fetchone(query, professor_id)


def professor_select_rating_distribution(professor_id):
    query = "SELECT * from get_professor_rating_distribution(%s)"
    return fetchone(query, professor_id)


def professor_search(
    page: int = None,
    limit: int = None,
):
    query = "SELECT id, name, email FROM users WHERE is_professor = true"
    if page and limit:
        query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    return fetchall(query)


def professor_search_count():
    query = "SELECT COUNT(*) FROM users WHERE is_professor = true"
    return fetchone(query)[0]


def professor_search_by_similarity(query: str, page: int = None, limit: int = None):
    # TODO - make similarity threshold configurable
    sql_query = f"SELECT id, name, email FROM users WHERE is_professor = true AND similarity(name, %s) > 0.2 ORDER BY similarity(name, %s) DESC"
    if page and limit:
        sql_query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    return fetchall(sql_query, query, query)


def professor_search_by_similarity_count(query: str):
    # TODO - make similarity threshold configurable
    sql_query = f"SELECT COUNT(*) FROM users WHERE is_professor = true AND similarity(name, %s) > 0.2"
    return fetchone(sql_query, query)[0]


def professor_search_by_similarity_tags(query: str):
    # TODO - make similarity threshold configurable
    sql_query = """
        SELECT unnest AS tag, COUNT(*) AS count FROM (
            SELECT unnest(tags) FROM users u
            LEFT JOIN reviews r ON r.professor_id = u.id
            WHERE u.is_professor = true AND similarity(u.name, %s) > 0.2
        ) GROUP BY unnest
    """
    return fetchall(sql_query, query)


def professor_search_by_last_name(
    last_name_start: str, page: int = None, limit: int = None
):
    sql_query = f"""
        SELECT id, name, email FROM users
        WHERE is_professor = true AND
        name ~ ' {last_name_start}[^\\s]*$' ORDER BY name ASC
    """
    if page and limit:
        sql_query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    return fetchall(sql_query)


def professor_search_by_last_name_count(last_name_start: str):
    sql_query = f"""
        SELECT COUNT(*) FROM users
        WHERE is_professor = true AND
        name ~ ' {last_name_start}[^\\s]*$'
    """
    return fetchone(sql_query)[0]


def professor_select_most_visited(limit: int, start_time: str):
    """
    Select the most visited professors that were visited after
    start_time
    """
    query = f"""
        SELECT professor_id, COUNT(*) AS visits FROM professor_visits
        WHERE created_at > %s
        GROUP BY (professor_id) 
        ORDER BY COUNT(*) DESC
        LIMIT %s
    """

    return fetchall(query, start_time, limit)
