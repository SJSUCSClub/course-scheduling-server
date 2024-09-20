from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.services import get_paginated_schedules_by_professor
from .utils import validate_page_limit, try_response


@api_view(["GET"])
@try_response
def professor_schedules_view(request, professor_id):
    json_data = get_paginated_schedules_by_professor(
        professor_id=professor_id,
        **validate_page_limit(request),
    )

    return JsonResponse(json_data)
