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
    course_search_by_filters_departments,
    course_search_by_similarity_departments,
)


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
):
    if query:
        items = course_search_by_similarity(query, department, page=page, limit=limit)
        total_results = course_search_by_similarity_count(query, department)
        departments = course_search_by_similarity_departments(query, department)
    else:
        items = course_search_by_filters(department, page=page, limit=limit)
        total_results = course_search_by_filters_count(department)
        departments = course_search_by_filters_departments(department)
    return {
        "items": items,
        "total_results": total_results,
        "page": page,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
        "filters": {"departments": departments},
    }
