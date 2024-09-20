from core.daos.reviews import (
    reviews_select,
    reviews_select_count,
    review_select_upvotes,
    review_select_tags,
)


def get_paginated_reviews_by_course(
    dept: str, course_number: str, limit: int, page: int, tags=[]
):
    reviews = reviews_select(
        dept,
        course_number,
        tags=tags,
        limit=limit,
        page=page,
    )

    for review in reviews:
        votes = review_select_upvotes(review["id"])
        review["votes"] = votes
        review["comments"] = None

    total_results = reviews_select_count(dept, course_number, tags=tags)
    tags = review_select_tags(department=dept, course_number=course_number, tags=tags)

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
