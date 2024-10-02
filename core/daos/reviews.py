from django.db import connection
from core.daos.utils import to_where, fetchall, fetchone, get
from typing import List, Dict, Union, Literal


def process_tags(tags: str) -> List[str]:
    return [tag.strip('"{} ') for tag in tags.split(",")]


def reviews_select(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    tags: List[str] = [],
    limit: int = None,
    page: int = None,
    user_id: str = None
):
    """
    Select reviews from the database with any of the given filters

    Args:
        department: string - the department of the course
        course_number: string - the number of the course
        professor_id: string - the id of the professor
        tags: List[str] - the tags of the review
        limit: int - the number of results to return per page; only effective if page is also provided
        page: int - the 1-indexed page number; only effective if limit is also provided

    Returns:
        out: List[dict] - A list of reviews
    """
    args = locals()
    page = args.pop("page")
    limit = args.pop("limit")
    user_id = args.pop("user_id")
    query = """
        SELECT r.*, u.name AS reviewer_name, u.username AS reviewer_username, p.id AS professor_id, p.name AS professor_name, p.email AS professor_email, urc.vote_type AS user_vote
        FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id
        INNER JOIN users p ON r.professor_id = p.id
        LEFT JOIN user_review_critique urc ON urc.review_id = r.id AND urc.user_id = {user_id}
    """
    query += to_where(**args)

    if page and limit:
        query += f" LIMIT {limit} OFFSET {(page - 1 ) * limit}"

    ret = fetchall(query, *list(filter(lambda x: x is not None, args.values())))
    for el in ret:
        el["tags"] = process_tags(el["tags"])
        el["vote"] = el.get("upvote", None)
    print(ret)
    return ret


def reviews_select_count(
    department: str = None,
    course_number: str = None,
    professor_id: str = None,
    tags: List[str] = [],
):
    args = locals()
    query = """SELECT COUNT(*) FROM reviews""" + to_where(**args)
    return fetchone(query, *list(filter(lambda x: x is not None, args.values())))[0]


def review_select_upvotes(review_id):
    votes = {"upvotes": 0, "downvotes": 0}

    with connection.cursor() as cursor:
        query = """
            SELECT upvote, COUNT(*)
            FROM user_review_critique
            WHERE review_id=%s
            GROUP BY upvote;
        """
        cursor.execute(query, (review_id,))
        results = cursor.fetchall()
        for upvote, count in results:
            if upvote:
                votes["upvotes"] = count
            else:
                votes["downvotes"] = count

    return votes


def review_select_comments(review_id):
    return get("comments", {"review_id": review_id})


def review_select_tags(
    **kwargs,
) -> List[Dict[Union[Literal["tag"], Literal["count"]], Union[str, int]]]:
    """
    Select the tags from the database with any of the given filters

    Args:
        department: string - the department of the course
        course_number: string - the number of the course
        professor_id: string - the id of the professor

    Returns:
        tags: List[dict] - A list of tags in the form {"tag": str, "count": int}
    """
    inner_query = "SELECT unnest(tags) FROM reviews" + to_where(**kwargs)
    query = f"""
        SELECT unnest AS tag, COUNT(unnest) AS count FROM ({inner_query}) GROUP BY unnest;
    """
    return fetchall(query, *list(filter(lambda x: x is not None, kwargs.values())))
