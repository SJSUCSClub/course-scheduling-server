from core.constants import DEFAULT_PAGE, DEFAULT_PAGE_LIMIT
from django.http import JsonResponse
import traceback
import sys


def validate_page_limit(request):
    page = request.GET.get("page") or DEFAULT_PAGE
    limit = request.GET.get("limit") or DEFAULT_PAGE_LIMIT

    return {"page": int(page), "limit": int(limit)}


def try_response(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(traceback.format_exc(), file=sys.stderr)
            return JsonResponse({"message": e.args}, status=500)

    return wrapper
