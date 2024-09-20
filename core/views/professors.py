from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.daos import professor_select_summary
from core.services import (
    get_paginated_schedules_by_professor,
    get_professor_reviews_stats,
    get_paginated_reviews_by_professor,
    get_professor_search_results,
)
from .utils import validate_page_limit, try_response


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
    json_data = professor_select_summary(professor_id=professor_id)
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
    )

    return JsonResponse(json_data)


@api_view(["GET"])
@try_response
def professor_search_view(request):
    json_data = get_professor_search_results(
        **validate_page_limit(request),
        query=request.GET.get("query", None),
    )

    return JsonResponse(json_data)