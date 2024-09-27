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
        db_status = "healthy"
    except OperationalError:
        db_status = "unhealthy"
    end_time = time.time()

    # Database Status
    db_check_time = end_time - start_time
    if db_check_time > db_timeout:
        db_status = "unhealthy"

    # Overall Status
    overall_status = "healthy" if db_status == "healthy" else "unhealthy"
    response_data = {
        "status": overall_status,
        "database": {
            "status": db_status,
            "time": db_check_time
        },
    }
    status_code = 200 if overall_status == "healthy" else 503
    return JsonResponse(response_data, status=status_code)
