from core.constants import DEFAULT_PAGE, DEFAULT_PAGE_LIMIT
from django.http import JsonResponse, HttpRequest
import traceback
import sys
import json

def validate_page_limit(request: HttpRequest):
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


def validate_user(request: HttpRequest) -> str:
    if not request.user.is_authenticated:
        return None
    return request.user.email.removesuffix("@sjsu.edu")


def validate_body(request: HttpRequest) -> dict:
    return request.data

def format_tags(tags):
    # Convert tags list to string
    tags = str(tags)
    tags = tags.replace("[","{").replace("]","}").replace("'","\"")
    return tags
