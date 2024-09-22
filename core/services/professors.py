from core.daos import (
    professor_select_average_rating,
    professor_select_average_quality,
    professor_select_average_ease,
    professor_select_average_grade,
    professor_select_rating_distribution,
    professor_select_quality_distribution,
    professor_select_ease_distribution,
    professor_select_grade_distribution,
    professor_select_total_reviews,
    professor_select_take_again_percent,
    review_select_tags,
    professor_search,
    professor_search_count,
    professor_search_by_similarity,
    professor_search_by_similarity_count,
    professor_search_by_similarity_tags,
)


def get_professor_reviews_stats(professor_id: str):
    return {
        "avg_rating": professor_select_average_rating(professor_id),
        "avg_quality": professor_select_average_quality(professor_id),
        "avg_ease": professor_select_average_ease(professor_id),
        "avg_grade": professor_select_average_grade(professor_id),
        "rating_distribution": professor_select_rating_distribution(professor_id),
        "quality_distribution": professor_select_quality_distribution(professor_id),
        "ease_distribution": professor_select_ease_distribution(professor_id),
        "grade_distribution": professor_select_grade_distribution(professor_id),
        "total_reviews": professor_select_total_reviews(professor_id),
        "take_again_percent": professor_select_take_again_percent(professor_id),
        "tags": review_select_tags(professor_id=professor_id),
    }


def get_professor_search_results(page: int, limit: int, query: str = None):
    if query:
        items = professor_search_by_similarity(query, page=page, limit=limit)
        total_results = professor_search_by_similarity_count(query)
        tags = professor_search_by_similarity_tags(query)
    else:
        items = professor_search(page=page, limit=limit)
        total_results = professor_search_count()
        tags = review_select_tags()
    return {
        "items": items,
        "total_results": total_results,
        "page": page,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
        "filters": {"tags": tags},
    }
