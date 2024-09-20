from .utils import fetchone, fetchone_as_dict, fetchall


# SUMMARY
def professor_select_summary(professor_id):
    query = "SELECT id, name, email FROM users WHERE id = %s"
    return fetchone_as_dict(query, professor_id)


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
    sql_query = f"SELECT id, name, email FROM users WHERE is_professor = true AND similarity(name, %s) > 0.4 ORDER BY similarity(name, %s) DESC"
    if page and limit:
        sql_query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    return fetchall(sql_query, query, query)


def professor_search_by_similarity_count(query: str):
    # TODO - make similarity threshold configurable
    sql_query = f"SELECT COUNT(*) FROM users WHERE is_professor = true AND similarity(name, %s) > 0.4"
    return fetchone(sql_query, query)[0]
