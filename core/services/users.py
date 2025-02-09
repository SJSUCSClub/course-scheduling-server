from core.daos.utils import get, update, insert, delete, insert_no_dupes
from datetime import datetime
from core.daos import (
    review_select_upvotes,
    user_select_reviews,
    user_select_comments,
    user_select_flagged_reviews,
    user_select_voted_reviews,
    user_voted_review,
)
from core.services.utils import format_tags


def get_user_profile(user_id: str):
    reviews = user_select_reviews(user_id)
    for review in reviews:
        review["votes"] = review_select_upvotes(review["id"])
        review["user_vote"] = user_voted_review(user_id=user_id, review_id=review["id"])

        # don't send user's actual name if the review is anonymous
        if review["is_user_anonymous"]:
            review["reviewer_name"] = None
            review["user_id"] = None
    print(reviews)
    flagged_reviews = user_select_flagged_reviews(user_id)
    for review in flagged_reviews:
        review["votes"] = review_select_upvotes(review["id"])
        review["user_vote"] = user_voted_review(user_id=user_id, review_id=review["id"])
    reviews_voted = user_select_voted_reviews(user_id)
    for review in reviews_voted:
        review["votes"] = review_select_upvotes(review["id"])
        review["user_vote"] = user_voted_review(user_id=user_id, review_id=review["id"])
    return {
        "reviews": reviews,
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
            "department": data["department"],
        },
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
            "is_user_anonymous": data["is_user_anonymous"],
        }
    )


def update_review(user_id, review_id, **data):
    allowed_keys = ["tags", "content", "quality", "ease", "grade", "take_again", "is_user_anonymous"]
    data = {key: value for key, value in data.items() if key in allowed_keys}
    if "tags" in data:
        data["tags"] = format_tags(data.get("tags", []))
    data["updated_at"] = datetime.now()
    return update("reviews",data,{"user_id": user_id, "id": review_id})


def insert_comment(user_id, review_id, content):
    return insert(
        "comments",
        {
            "user_id": user_id,
            "review_id": review_id,
            "content": content,
        }
    )


def update_comment(user_id, comment_id, review_id, content):
    return update(
        "comments",
        {"content": content, "updated_at": datetime.now()},
        {"user_id": user_id, "review_id": review_id, "id": comment_id}
    )


def insert_review_flag(user_id, review_id, reason):
    return insert_no_dupes(
        "flag_reviews",
        {
            "user_id": user_id,
            "review_id": review_id,
            "reason": reason
        }, ["user_id","review_id"]
    )


def update_review_flag(user_id, flag_id, review_id, reason):
    return update(
        "flag_reviews",
        {"reason": reason, "updated_at": datetime.now()},
        {"user_id": user_id, "review_id": review_id, "id": flag_id}
    )


def insert_vote(user_id, review_id, vote):
    where_condition = {"user_id": user_id, "review_id": review_id}
    if vote is None:
        return delete("user_review_critique", where_condition)
    existing_vote = get("user_review_critique", where_condition)
    if existing_vote:
        return update("user_review_critique", {"upvote": vote}, where_condition)
    return insert("user_review_critique", {**where_condition, "upvote": vote})


def insert_comment_flag(user_id, comment_id, reason):
    return insert_no_dupes(
        "flag_comments",
        {
            "user_id": user_id,
            "comment_id": comment_id,
            "reason": reason,
        }, ["user_id","comment_id"]
    )


def update_comment_flag(user_id, flag_id, comment_id, reason):
    return update(
        "flag_comments",
        {"reason": reason, "updated_at": datetime.now()},
        {"user_id": user_id, "comment_id": comment_id, "id": flag_id},
    )


