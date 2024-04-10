from django.shortcuts import render
import json
from core.sql_funcs import *
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db import connection
from core.models import Users, Courses, Reviews, Schedules
from core.serializers import CourseSerialized, UsersSerialized, ReviewsSerialized, ReviewCommentsSerialized, SchedulesSerialized
from rest_framework.decorators import api_view
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def sql_courses(request):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM Courses")
    #     all_courses = cursor.fetchall()
    #     rows = [x[0] for x in cursor.description]

    # json_data = []
    # for result in all_courses:
    #     # json_data = dict(zip(rows, all_courses))
    #     json_data.append(dict(zip(rows, result)))

    # print(json_data[0])
    json_data = general_statements('Courses')
    course_json = json.dumps(json_data)

    return JsonResponse(json.loads(course_json), safe=False)


@api_view(['GET'])
def sql_schedules(request):
    id = request.GET.get('id')

    if id is not None:
        json_data = where('Schedules', {'class_number': id})
    else:
        json_data = general_statements('Schedules')
    # with connection.cursor() as cursor:
    #     if id is not None:
    #         cursor.execute(
    #             "SELECT * FROM Schedules WHERE class_number=%s", [id])
    #         rows = [x[0] for x in cursor.description]
    #         schedules = cursor.fetchone()
    #         # print(schedules[14])

    #         ''' Querying for professors per schedule '''

    #         json_data = dict(zip(rows, schedules))

    #     else:
    #         cursor.execute("SELECT * FROM Schedules")
    #         rows = [x[0] for x in cursor.description]
    #         schedules = cursor.fetchall()
    #         json_data = []
    #         for result in schedules:
    #             # json_data = dict(zip(rows, all_courses))
    #             json_data.append(dict(zip(rows, result)))
    print(json_data)
    if json_data is None:
        return JsonResponse({"message": "An error occurred"}, status=status.HTTP_404_NOT_FOUND)
    schedules_json = json.dumps(json_data)
    return JsonResponse(json.loads(schedules_json), safe=False)


def sql_reviews(request):
    id = request.GET.get('id')

    with connection.cursor() as cursor:
        if id is not None:
            cursor.execute('SELECT ')


@api_view(['GET'])
def courses(request):
    if request.method == 'GET':
        all_courses = Courses.objects.all()

        course_serializer = CourseSerialized(all_courses, many=True)
        return JsonResponse(course_serializer.data, safe=False)


@api_view(['GET'])
def course(request, csn, dept):
    try:
        one_course = Courses.objects.get(
            course_number=csn, department=dept)
    except Courses.DoesNotExist:
        return JsonResponse({"message": "This course doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # courseNumber = request.query_params.get('csn', None)
        # dept = request.query_params.get('dept', None)

        course_serializer = CourseSerialized(one_course)
        return JsonResponse(course_serializer.data, safe=False)


@api_view(['GET'])
def schedule(request, csn, dept):
    try:
        schedule_list = Schedules.objects.get(
            course_number=csn, department=dept)
    except Schedules.DoesNotExist:
        return JsonResponse({"message": "This course is not featured in our schedules"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':

        schedule_serializer = SchedulesSerialized(schedule_list)
        return JsonResponse(schedule_serializer.data, safe=False)


@api_view(['GET'])
def coursereviews(request, csn, dept):
    try:
        reviews = Reviews.objects.filter(
            course_number=csn, department=dept)
    except Reviews.DoesNotExist:
        return JsonResponse({"message": "There are currently no reviews for this course"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        reviews_serialized = ReviewCommentsSerialized(reviews, many=True)

        return JsonResponse(reviews_serialized.data, status=status.HTTP_200_OK, safe=False)
