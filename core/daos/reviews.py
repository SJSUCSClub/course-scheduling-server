from django.db import connection


def reviews_select_paginated_by_course(dept, course_number, limit, page, tags=[]):
    with connection.cursor() as cursor:
        query = """
            select r.*, u.name as reviewer_name, u.username as reviewer_username, p.id as professor_id, p.name as professor_name, p.email as professor_email
            from reviews r
            left join users u on r.user_id = u.id
            inner join users p on r.user_id = p.id
            where r.department=%s and course_num=%s and r.tags @> %s::tag_enum[]
            limit %s
            offset %s;
        """
        cursor.execute(query, (dept, course_number, tags, limit, (page - 1) * limit))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def review_select_upvotes(review_id):
    votes = {"upvotes": 0, "downvotes": 0}

    with connection.cursor() as cursor:
        query = """
            select upvote, count(*)
            from user_review_critique
            where review_id=%s
            group by upvote;
        """
        cursor.execute(query, (review_id,))
        print(cursor.fetchall())

    return votes


def review_select_comments(review_id):
    pass
