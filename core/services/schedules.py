from core.daos import (
    schedule_select,
    schedule_select_counts,
    schedule_search_by_filters,
    schedule_search_by_filters_count,
    schedule_search_by_similarity,
    schedule_search_by_similarity_count,
)


def get_paginated_schedules_by_course(
    department: str, course_number: str, limit: int, page: int
):
    total_results = schedule_select_counts(department, course_number)
    return {
        "items": schedule_select(department, course_number, page=page, limit=limit),
        "total_results": total_results,
        "page": page,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
    }


def get_paginated_schedules_by_professor(
    professor_id: str, limit: int = None, page: int = None
):
    total_results = schedule_select_counts(professor_id=professor_id)
    return {
        "items": schedule_select(professor_id=professor_id, page=page, limit=limit),
        "total_results": total_results,
        "page": page,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
    }


def get_schedules_search_results(
    query: str = None,
    term: str = None,
    year: str = None,
    professor_name: str = None,
    course_number: str = None,
    department: str = None,
    mode_of_instruction: str = None,
    units: str = None,
    page: int = None,
    limit: int = None,
):
    args = locals()  # store all args in a dict
    page = args.pop("page")
    limit = args.pop("limit")
    query = args.pop("query")
    filter_categories = list(args.keys())
    if query:
        search_fn = schedule_search_by_similarity
        count_fn = schedule_search_by_similarity_count
        args["query"] = query
    else:
        search_fn = schedule_search_by_filters
        count_fn = schedule_search_by_filters_count

    items = search_fn(**args, page=page, limit=limit)
    total_results = count_fn(**args, count_by=None)
    filters = {key: count_fn(**args, count_by=key) for key in filter_categories}

    total_results = total_results[0]["count"]
    return {
        "items": items,
        "total_results": total_results,
        "page": page,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
        "filters": filters,
    }
