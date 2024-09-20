from core.daos import schedule_select, schedule_select_counts


def get_paginated_schedules_by_course(
    department: str, course_number: str, limit: int, page: int
):
    total_results = schedule_select_counts(department, course_number)
    return {
        "schedules": schedule_select(department, course_number, page=page, limit=limit),
        "total_results": total_results,
        "page": page,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
    }


def get_paginated_schedules_by_professor(
    professor_id: str, limit: int = None, page: int = None
):
    total_results = schedule_select_counts(professor_id=professor_id)
    return {
        "schedules": schedule_select(professor_id=professor_id, page=page, limit=limit),
        "total_results": total_results,
        "page": page,
        "pages": total_results // limit + (1 if total_results % limit > 0 else 0),
    }
