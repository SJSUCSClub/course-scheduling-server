from django.db import connection


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
