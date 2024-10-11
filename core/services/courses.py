from datetime import datetime, timedelta
from core.daos import (
    course_select_average_rating,
    course_select_average_quality,
    course_select_average_ease,
    course_select_average_grade,
    course_select_rating_distribution,
    course_select_quality_distribution,
    course_select_ease_distribution,
    course_select_grade_distribution,
    course_select_total_reviews,
    course_select_take_again_percent,
    course_search_by_filters,
    course_search_by_filters_count,
    course_search_by_similarity,
    course_search_by_similarity_count,
    course_select_summary,
    course_insert_view,
    course_select_most_visited,
)


def get_course_most_visited():
    last_month = datetime.now() - timedelta(weeks=4)
    most_visited = course_select_most_visited(
        3, last_month.isoformat(sep=" ", timespec="seconds")
    )
    if len(most_visited) == 0:
        # no one visited our site in the past month...
        # so just return the most visited overall (starting from epoch)
        most_visited = course_select_most_visited(3, "1970-01-01 00:00:00")
    return {
        "most_visited": [
            get_course_reviews_stats(el["department"], el["course_number"])
            | course_select_summary(el["department"], el["course_number"])
            | {"visits": el["visits"]}
            for el in most_visited
        ]
    }


def get_course_summary(dept, course_number):
    """
    Inserts a visit into courses_visits and returns the summary
    """
    course_insert_view(dept, course_number)
    return course_select_summary(dept, course_number)


def get_course_reviews_stats(dept, course_number):
    return {
        "department": dept,
        "course_number": course_number,
        "avg_rating": course_select_average_rating(dept, course_number),
        "avg_quality": course_select_average_quality(dept, course_number),
        "avg_ease": course_select_average_ease(dept, course_number),
        "avg_grade": course_select_average_grade(dept, course_number),
        "rating_distribution": course_select_rating_distribution(dept, course_number),
        "quality_distribution": course_select_quality_distribution(dept, course_number),
        "ease_distribution": course_select_ease_distribution(dept, course_number),
        "grade_distribution": course_select_grade_distribution(dept, course_number),
        "total_reviews": course_select_total_reviews(dept, course_number),
        "take_again_percent": course_select_take_again_percent(dept, course_number),
    }


def get_course_search_results(
    page: int,
    limit: int,
    query: str = None,
    department: str = None,
    units: str = None,
    satisfies_area: str = None,
):
    args = locals()
    page = args.pop("page")
    limit = args.pop("limit")
    query = args.pop("query")
    search_fn = course_search_by_filters
    count_fn = course_search_by_filters_count
    if query:
        args["query"] = query
        search_fn = course_search_by_similarity
        count_fn = course_search_by_similarity_count

    items = search_fn(**args, page=page, limit=limit)
    total_results = count_fn(**args)[0]["count"]
    departments = count_fn(**args, count_by="department")
    units = count_fn(**args, count_by="units")
    satisfies_area = count_fn(**args, count_by="satisfies_area")

    return {
        "items": items,
        "total_results": total_results,
        "page": page,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
        "filters": {
            "departments": departments,
            "units": units,
            "satisfies_area": satisfies_area,
        },
    }
