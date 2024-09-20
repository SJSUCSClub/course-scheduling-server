from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.daos import course_select_summary
from core.services import (
    get_paginated_reviews_by_course,
    get_paginated_schedules_by_course,
)
from .query_validation import validate_page_limit


@api_view(["GET"])
def course_summary_view(request, department, course_number):
    try:
        json_data = course_select_summary(department, course_number)

        return JsonResponse(json_data)
    except Exception as e:
        return JsonResponse({"message": e.args}, status=500)


@api_view(["GET"])
def course_schedules_view(request, department, course_number):
    try:
        json_data = get_paginated_schedules_by_course(
            department,
            course_number,
            **validate_page_limit(request),
        )

        return JsonResponse(json_data)
    except Exception as e:
        return JsonResponse({"message": e.args}, status=500)


@api_view(["GET"])
def course_reviews_view(request, department, course_number):
    try:
        json_data = get_paginated_reviews_by_course(
            department, course_number, **validate_page_limit(request)
        )

        return JsonResponse(json_data)
    except Exception as e:
        return JsonResponse({"message": e.args}, status=500)
