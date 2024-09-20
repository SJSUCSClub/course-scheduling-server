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
