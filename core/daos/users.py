from django.db import connection
from core.daos.utils import get

def users_insert(name: str, id: str, email: str, is_professor: bool):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, id, email, is_professor, username) VALUES (%s, %s, %s, %s, generateUsername())",
            (name, id, email, is_professor),
        )
def user_select_reviews(user_id):
    return get("reviews", {"user_id":user_id})

def user_select_comments(user_id):
    return get("comments", {"user_id":user_id})

def user_select_flags(user_id):
    return get("flag_reviews", {"user_id":user_id})

def user_select_votes(user_id):
    return get("user_review_critique", {"user_id":user_id})

def user_voted_review(
    user_id: str,
    review_id: str
):
    review = get("user_review_critique",{
        "user_id":user_id,
        "review_id":review_id
    })
    vote = review[0]["upvote"] if len(review) > 0 else None
    return vote
    