from .utils import try_response, validate_page_limit
from django.http import JsonResponse
from rest_framework.decorators import api_view
from core.services import get_schedules_search_results


@api_view(["GET"])
@try_response
def schedule_search_view(request):
    json_data = get_schedules_search_results(
        **validate_page_limit(request),
        query=request.GET.get("query", None),
        department=request.GET.get("department", None),
        course_number=request.GET.get("course_number", None),
        professor_name=request.GET.get("professor_name", None),
        term=request.GET.get("term", None),
        year=request.GET.get("year", None),
        mode_of_instruction=request.GET.get("mode_of_instruction", None),
        units=request.GET.get("units", None),
    )

    return JsonResponse(json_data)
