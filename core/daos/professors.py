from django.db import connection


# SUMMARY
def professor_select_summary(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT id, name, email FROM users WHERE id = %s"
        cursor.execute(query, (professor_id,))
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))


# STATS
def professor_select_average_grade(professor_id):
    with connection.cursor() as cursor:
        print("prof: ", professor_id)
        query = "SELECT get_professor_average_grade(%s)"
        cursor.execute(query, (professor_id,))

        data = cursor.fetchone()[0]
        print("avg grade: ", data)
        return data


def professor_select_average_quality(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT get_professor_average_quality(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()[0]


def professor_select_average_ease(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT get_professor_average_ease(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()[0]


def professor_select_take_again_percent(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT get_professor_take_again_percent(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()[0]


def professor_select_total_reviews(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT get_professor_total_reviews(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()[0]


def professor_select_average_rating(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT get_professor_average_rating(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()[0]


def professor_select_ease_distribution(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT * from get_professor_ease_distribution(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()


def professor_select_grade_distribution(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT * from get_professor_grade_distribution(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()


def professor_select_quality_distribution(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT * from get_professor_quality_distribution(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()


def professor_select_rating_distribution(professor_id):
    with connection.cursor() as cursor:
        query = "SELECT * from get_professor_rating_distribution(%s)"
        cursor.execute(query, (professor_id,))
        return cursor.fetchone()
