from core.constants import DEFAULT_PAGE, DEFAULT_PAGE_LIMIT


def validate_page_limit(request):
    page = request.GET.get("page") or DEFAULT_PAGE
    limit = request.GET.get("limit") or DEFAULT_PAGE_LIMIT

    return {"page": int(page), "limit": int(limit)}
