from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.services import (
    get_paginated_reviews_by_course,
    get_paginated_schedules_by_course,
    get_course_reviews_stats,
    get_course_search_results,
    get_course_summary,
    get_course_most_visited,
)
from .utils import validate_user, validate_page_limit, try_response


@api_view(["GET"])
@try_response
def course_summary_view(request, department: str, course_number: str):
    json_data = get_course_summary(department.upper(), course_number)

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def course_reviews_stats_view(request, department: str, course_number: str):
    json_data = get_course_reviews_stats(department.upper(), course_number)

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def course_schedules_view(request, department: str, course_number: str):
    json_data = get_paginated_schedules_by_course(
        department.upper(),
        course_number,
        **validate_page_limit(request),
    )

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def course_reviews_view(request, department: str, course_number: str):
    json_data = get_paginated_reviews_by_course(
        department.upper(),
        course_number,
        **validate_page_limit(request),
        tags=request.GET.getlist("tags"),
        user_id=validate_user(request),
    )

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def course_search_view(request):
    json_data = get_course_search_results(
        **validate_page_limit(request),
        query=request.GET.get("query", None),
        department=request.GET.get("department", None),
        units=request.GET.get("units", None),
        satisfies_area=request.GET.get("satisfies_area", None),
    )

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def course_most_visited_view(request):
    return JsonResponse(get_course_most_visited())
