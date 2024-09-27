import time
from sqlite3 import OperationalError

from django.http import JsonResponse
from rest_framework.decorators import api_view

from ..daos import professor_select_summary


@api_view(['GET'])
def health_check(request):
    db_timeout = 5
    start_time = time.time()
    try:
        professor_select_summary("david.taylor")
        db_status = "Healthy"
    except OperationalError:
        db_status = "Unhealthy"
    end_time = time.time()

    # Database Status
    db_check_time = end_time - start_time
    if db_check_time > db_timeout:
        db_status = "Unhealthy"

    # Overall Status
    overall_status = "Healthy" if db_status == "Healthy" else "Unhealthy"
    response_data = {
        "Status": overall_status,
        "Database": {
            "Status": db_status,
            "Response_time": db_check_time
        },
    }
    status_code = 200 if overall_status == "Healthy" else 503
    return JsonResponse(response_data, status=status_code)
