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
