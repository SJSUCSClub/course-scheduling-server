from core.daos.reviews import (
    reviews_select,
    reviews_select_count,
    review_select_upvotes,
    review_select_tags,
    review_select_comments
)


def get_paginated_reviews_by_course(
    dept: str, course_number: str, limit: int, page: int, tags=[], user_id = None
):
    reviews = reviews_select(
        dept,
        course_number,
        tags=tags,
        limit=limit,
        page=page,
        user_id= user_id
    )

    for review in reviews:
        votes = review_select_upvotes(review["id"])
        review["votes"] = votes
        review["comments"] = review_select_comments(review["id"])

    total_results = reviews_select_count(dept, course_number, tags=tags)
    tags = review_select_tags(department=dept, course_number=course_number, tags=tags)

    return {
        "items": reviews,
        "total_results": total_results,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
        "page": page,
        "filters": {"tags": tags},
    }


def get_paginated_reviews_by_professor(
    professor_id: str, limit: int, page: int, tags=[]
):
    """
    Returns a paginated list of reviews for a professor

    Very similar to get_paginated_reviews_by_course
    """
    reviews = reviews_select(
        professor_id=professor_id,
        tags=tags,
        limit=limit,
        page=page,
    )

    for review in reviews:
        votes = review_select_upvotes(review["id"])
        review["votes"] = votes
        review["comments"] = None

    total_results = reviews_select_count(professor_id=professor_id, tags=tags)
    tags = review_select_tags(professor_id=professor_id, tags=tags)

    return {
        "items": reviews,
        "total_results": total_results,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
        "page": page,
        "filters": {"tags": tags},
    }


def get_paginated_reviews_with_comments_by_course(
    dept, course_number, limit, page, tags=[]
):
    reviews = get_paginated_reviews_by_course(dept, course_number, limit, page, tags=[])

    for review in reviews:
        pass
