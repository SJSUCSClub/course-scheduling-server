from core.constants import DEFAULT_PAGE, DEFAULT_PAGE_LIMIT
from django.http import JsonResponse, HttpRequest
import traceback
import sys
from datetime import datetime
from better_profanity import profanity

def validate_page_limit(request: HttpRequest):
    page = request.GET.get("page") or DEFAULT_PAGE
    limit = request.GET.get("limit") or DEFAULT_PAGE_LIMIT

    return {"page": int(page), "limit": int(limit)}


def try_response(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
            return JsonResponse({"message": "Bad request"}, status=400)

    return wrapper


def validate_user(request: HttpRequest) -> str:
    if not request.user:
        return None
    if not request.user.is_authenticated:
        return None
    return request.user.email.removesuffix("@sjsu.edu")


def validate_body(request: HttpRequest) -> dict:
    return request.data

def content_check(content: str):
    return profanity.contains_profanity(content)

def check_flag_immunity(item):
    flag_immune_until = item["flag_immune_until"]
    return flag_immune_until > datetime.now()