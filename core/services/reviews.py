from core.daos.reviews import reviews_select_paginated_by_course, review_select_upvotes
from core.constants import DEFAULT_PAGE, DEFAULT_PAGE_LIMIT


def get_paginated_reviews_by_course(
    dept: str, course_number: str, limit: int = None, page: int = None, tags=[]
):
    page = page or DEFAULT_PAGE
    limit = limit or DEFAULT_PAGE_LIMIT
    reviews = reviews_select_paginated_by_course(dept, course_number, limit, page, tags)

    for review in reviews:
        votes = review_select_upvotes(review.id)
        review["votes"] = votes
        review["comments"] = None

    return reviews


def get_paginated_reviews_with_comments_by_course(
    dept, course_number, limit, page, tags=[]
):
    reviews = get_paginated_reviews_by_course(dept, course_number, limit, page, tags=[])

    for review in reviews:
        pass
