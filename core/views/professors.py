from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.services import (
    get_paginated_schedules_by_professor,
    get_professor_reviews_stats,
    get_paginated_reviews_by_professor,
    get_professor_search_results,
    get_professor_summary,
    get_professor_most_visited,
)
from .utils import validate_user, validate_page_limit, try_response


@api_view(["GET"])
@try_response
def professor_schedules_view(request, professor_id):
    json_data = get_paginated_schedules_by_professor(
        professor_id=professor_id,
        **validate_page_limit(request),
    )

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def professor_summary_view(request, professor_id):
    json_data = get_professor_summary(professor_id=professor_id)
    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def professor_reviews_stats_view(request, professor_id):
    json_data = get_professor_reviews_stats(professor_id=professor_id)
    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def professor_reviews_view(request, professor_id):
    json_data = get_paginated_reviews_by_professor(
        professor_id=professor_id,
        **validate_page_limit(request),
        tags=request.GET.getlist("tags"),
        user_id=validate_user(request),
    )

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def professor_search_view(request):
    json_data = get_professor_search_results(
        **validate_page_limit(request),
        query=request.GET.get("query", None),
        startswith=request.GET.get("startswith", None),
    )

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def professor_most_visited_view(request):
    return JsonResponse(get_professor_most_visited())
