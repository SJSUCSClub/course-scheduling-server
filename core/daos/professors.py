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


def professor_select(
    page: int = None,
    limit: int = None,
):
    query = "SELECT id, name, email FROM users WHERE is_professor = true"

    if page and limit:
        query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    return fetchall(query)
