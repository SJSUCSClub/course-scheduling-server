from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.daos import course_select_summary
from core.services import (
    get_paginated_reviews_by_course,
    get_paginated_schedules_by_course,
    get_course_reviews_stats,
)
from .utils import validate_page_limit, try_response


@api_view(["GET"])
@try_response
def course_summary_view(request, department, course_number):
    json_data = course_select_summary(department, course_number)

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def course_reviews_stats_view(request, department, course_number):
    json_data = get_course_reviews_stats(department, course_number)

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def course_schedules_view(request, department, course_number):
    json_data = get_paginated_schedules_by_course(
        department,
        course_number,
        **validate_page_limit(request),
    )

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def course_reviews_view(request, department, course_number):
    json_data = get_paginated_reviews_by_course(
        department,
        course_number,
        **validate_page_limit(request),
        tags=request.GET.getlist("tags"),
    )

    return JsonResponse(json_data)
