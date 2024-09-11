from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.daos import course_select_summary, course_select_ease_distribution, course_select_grade_distribution, course_select_quality_distribution, course_select_rating_distribution, course_select_average_grade, course_select_average_ease, course_select_average_quality, course_select_average_rating, course_select_total_reviews, course_select_take_again_percent

@api_view(['GET'])
def course_summary_view(request, department, course_number):
    try:
        course_select_summary(department, course_number)
        json_data = course_select_summary(department, course_number)

        return JsonResponse(json_data)
    except Exception as e:
        return JsonResponse({"message": e.args}, status=500)
    