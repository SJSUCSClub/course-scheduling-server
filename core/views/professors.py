from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.services import get_paginated_schedules_by_professor
from .query_validation import validate_page_limit


@api_view(["GET"])
def professor_schedules_view(request, professor_id):
    try:
        json_data = get_paginated_schedules_by_professor(
            professor_id=professor_id,
            **validate_page_limit(request),
        )

        return JsonResponse(json_data)
    except Exception as e:
        return JsonResponse({"message": e.args}, status=500)
