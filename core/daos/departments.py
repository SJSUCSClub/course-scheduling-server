from .utils import fetchall


def departments_select_all():
    query = """
        SELECT d.abbr_dept, d.name, COUNT(*) FROM departments d
        LEFT JOIN courses c ON c.department = d.abbr_dept
        GROUP BY abbr_dept
        ORDER BY abbr_dept ASC
    """
    return fetchall(query)
