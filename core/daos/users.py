from django.db import connection
from core.daos.utils import get, fetchall
from typing import List

def process_tags(tags: str) -> List[str]:
    return [tag.strip('"{} ') for tag in tags.split(",")]

def users_insert(name: str, id: str, email: str, is_professor: bool):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, id, email, is_professor, username) VALUES (%s, %s, %s, %s, generateUsername())",
            (name, id, email, is_professor),
        )
def user_select_reviews(user_id):
    query = """
        SELECT r.*, u.name AS reviewer_name, u.username AS reviewer_username, p.id AS professor_id, p.name AS professor_name, p.email AS professor_email
        FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id
        INNER JOIN users p ON r.professor_id = p.id
        WHERE r.user_id = %s
    """
    ret = fetchall(query, user_id)
    for el in ret:
        el["tags"] = process_tags(el["tags"])
    return ret

def user_select_comments(user_id):
    return get("comments", {"user_id":user_id})

def user_select_flagged_reviews(user_id):
    query = """
        SELECT r.*, u.name AS reviewer_name, u.username AS reviewer_username, p.id AS professor_id, p.name AS professor_name, p.email AS professor_email
        FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id
        INNER JOIN users p ON r.professor_id = p.id
        WHERE r.id IN (
            SELECT review_id FROM flag_reviews WHERE user_id = %s
        )
    """
    ret = fetchall(query, user_id)
    for el in ret:
        el["tags"] = process_tags(el["tags"])
    return ret

def user_select_voted_reviews(user_id):
    query = """
        SELECT r.*, u.name AS reviewer_name, u.username AS reviewer_username, p.id AS professor_id, p.name AS professor_name, p.email AS professor_email
        FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id
        INNER JOIN users p ON r.professor_id = p.id
        WHERE r.id IN (
            SELECT review_id FROM user_review_critique WHERE user_id = %s
        )
    """
    ret = fetchall(query, user_id)
    for el in ret:
        el["tags"] = process_tags(el["tags"])
    return ret

def user_voted_review(
    user_id: str,
    review_id: str
):
    if user_id is None:
        return None
    review = get("user_review_critique",{
        "user_id":user_id,
        "review_id":review_id
    })
    vote = review[0]["upvote"] if len(review) > 0 else None
    return vote
