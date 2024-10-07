from core.daos.utils import get,update,insert,delete
from datetime import datetime
from core.daos import (
    review_select_upvotes,
    user_select_reviews,
    review_select_comments,
    user_select_comments,
    user_select_flagged_reviews,
    user_select_voted_reviews,
    user_voted_review
)
from core.views.utils import format_tags

def get_user_profile(user_id: str):
    reviews = user_select_reviews(user_id)
    for review in reviews:
        review["votes"] = review_select_upvotes(review["id"])
        review["user_vote"] = user_voted_review(
            user_id=user_id,
            review_id=review["id"]
        )
    flagged_reviews = user_select_flagged_reviews(user_id)
    for review in flagged_reviews:
        review["votes"] = review_select_upvotes(review["id"])
        review["user_vote"] = user_voted_review(
            user_id=user_id,
            review_id=review["id"]
        )
    reviews_voted = user_select_voted_reviews(user_id)
    for review in reviews_voted:
        review["votes"] = review_select_upvotes(review["id"])
        review["user_vote"] = user_voted_review(
            user_id=user_id,
            review_id=review["id"]
        )
    return {
        "reviews":reviews,
        "comments": user_select_comments(user_id),
        "flagged_reviews": flagged_reviews,
        "reviews_voted": reviews_voted,
    }
def get_existing_review(user_id, data):
    return get(
        "reviews",
        {
            "user_id": user_id,
            "professor_id": data["professor_id"],
            "course_number": data["course_number"],
            "department":data["department"]
        }
    )
def insert_review(user_id, data):
    return insert(
        "reviews",
        {
            "user_id": user_id,
            "professor_id": data["professor_id"],
            "course_number": data["course_number"],
            "department": data["department"],
            "content": data["content"],
            "quality": data["quality"],
            "ease": data["ease"],
            "grade": data["grade"],
            "take_again": data["take_again"],
            "tags": format_tags(data["tags"]),
            "is_user_anonymous": data["is_user_anonymous"]
        }
    )

def update_review(user_id, review_id, data):
    return update(
        "reviews",
        {
            "professor_id": data["professor_id"],
            "course_number": data["course_number"],
            "department": data["department"],
            "content": data["content"],
            "quality": data["quality"],
            "ease": data["ease"],
            "grade": data["grade"],
            "take_again": data["take_again"],
            "tags": format_tags(data["tags"]),
            "is_user_anonymous": data["is_user_anonymous"],
        },
        {"user_id": user_id, "id": review_id},
    )

def insert_comment(user_id, data):
    return insert(
        "comments",
        {
            "user_id": user_id,
            "review_id": data["review_id"],
            "content": data["content"],
        },
    )

def update_comment(user_id, comment_id, review_id, data):
    return update(
        "comments",
        {"content": data["content"], "updated_at": datetime.now()},
        {"user_id": user_id, "review_id": review_id, "id": comment_id},
    )

def insert_flag(user_id, data):
    return insert(
        "flag_reviews",
        {
            "user_id": user_id,
            "review_id": data["review_id"],
            "reason": data["reason"],
        },
    )

def update_flag(user_id, flag_id, review_id, data):
    return update(
        "flag_reviews",
        {"reason": data["reason"]},
        {"user_id": user_id, "review_id": review_id, "id": flag_id},
    )


def insert_vote(user_id, data):
    if data["vote"] == None:
        return delete(
            "user_review_critique",
            {"user_id": user_id, "review_id": data["review_id"]}
        )
    check = get(
        "user_review_critique",
        {"user_id": user_id, "review_id": data["review_id"]}
    )
    if check:
        return update(
            "user_review_critique",
            {"upvote": data["vote"]},
            {"user_id": user_id, "review_id": data["review_id"]},
        )
    return insert(
        "user_review_critique",
        {
            "user_id": user_id,
            "review_id": data["review_id"],
            "upvote": data["vote"]
        },
    )
