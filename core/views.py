from django.shortcuts import render
import json
from core.sql_funcs import *
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db import connection
from core.models import Users, Courses, Reviews, Schedules
# from core.serializers import CourseSerialized, UsersSerialized, ReviewsSerialized, ReviewCommentsSerialized, SchedulesSerialized
from rest_framework.decorators import api_view
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET'])
def sql_courses(request):
    csn = request.GET.get('course_number')
    dept = request.GET.get('department')

    if csn is not None and dept is not None:
        json_data = where(
            'Courses', {'course_number': csn, 'department': dept})
    else:
        json_data = general_statements('Courses')

    return JsonResponse(json_data, safe=False)


@api_view(['GET'])
def sql_schedules(request):
    csn = request.GET.get('course_number')
    dept = request.GET.get('department')

    if csn is not None and dept is not None:
        json_data = where(
            'Schedules', {'course_number': csn, 'department': dept})

        final_arr = []
        for json_obj in json_data:
            if json_obj['professor_id'] is not None:
                prof_data = where(
                    'Users', {'id': json_obj['professor_id']}, ['name'])
                merged = [json_obj, prof_data[0]]
                final_json = row_merge(merged)
                final_arr.append(final_json)
            else:
                final_arr.append(json_obj)

    else:
        final_arr = general_statements('Schedules')

    # if json_data is None:
    #     return JsonResponse({"message": "An error occurred"}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse(final_arr, safe=False)


@api_view(['GET'])
def sql_reviews(request):
    csn = request.GET.get('course_number')
    dept = request.GET.get('department')
    comments = request.GET.get('comments')

    if csn is not None and dept is not None:
        json_data = where(
            'Reviews', {'course_number': csn, 'department': dept})

        final_arr = []
        for json_obj in json_data:

            ''' Get review critics '''
            if json_obj['id'] is not None:
                critics = where('user_review_critique', {
                                'review_id': json_obj['id']}, ['upvote'])
                if comments is not None and comments:
                    comments = where('comments', {
                        'review_id': json_obj['id']})
                    json_obj = row_merge(
                        [json_obj, {'critics': critics}, {'comments': comments}])
                else:
                    json_obj = row_merge([json_obj, {'critics': critics}])

            ''' Get professor email and name  '''
            if json_obj['professor_id'] is not None:
                prof = where('users', {'id': json_obj['professor_id']}, [
                             'name', 'email'])
                json_obj = row_merge([json_obj, prof[0]])

            ''' Obtain username and name'''
            if json_obj['user_id'] is not None:
                user = where('users', {'id': json_obj['user_id']}, [
                             'username', 'name'])
                json_obj = row_merge([json_obj, user[0]])

            final_arr.append(json_obj)

        return JsonResponse(final_arr, safe=False)

    else:
        return JsonResponse({"message": " course_number and or department not specified"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def review_stats(request):
    csn = request.GET.get('course_number')
    dept = request.GET.get('department')

    if csn is not None and dept is not None:

        final_json = auxiliary_json(dept, csn)
        return JsonResponse(final_json, safe=False)


@api_view(['GET'])
def summary(request):
    csn = request.GET.get('course_number')
    dept = request.GET.get('department')
    if csn is not None and dept is not None:
        json_data = where(
            'Courses', {'course_number': csn, 'department': dept})

        print(json_data)
        if len(json_data) > 0:
            partial_json = auxiliary_json(dept, csn)
            finalized_json = row_merge([json_data[0], partial_json])

            return JsonResponse(finalized_json, safe=False)
        else:
            return JsonResponse({"message": "Specified course not found"}, status=status.HTTP_404_NOT_FOUND)

    else:
        return JsonResponse({"message": " course_number and or department not specified"}, status=status.HTTP_404_NOT_FOUND)


''' In the event we need to pull all the comments pertaining to a certain course'''


@api_view(['GET'])
def review_comments(request):
    csn = request.GET.get('course_number')
    dept = request.GET.get('department')

    if csn is not None and dept is not None:
        review_ids = where(
            'Reviews', {'course_number': csn, 'department': dept}, ['id'])

        total_comments = []
        for id in review_ids:
            comments = where('Comments', {'review_id': id})
            total_comments += comments

        return JsonResponse(total_comments, safe=False)

    return JsonResponse({"message": " course_number and or department not specified"}, status=status.HTTP_404_NOT_FOUND)


def auxiliary_json(dept, csn):
    with connection.cursor() as cursor:
        ''' Initial averages '''
        query = 'SELECT get_course_average_grade(%s, %s), get_course_average_quality(%s, %s), get_course_average_ease(%s, %s),get_course_take_again_percent(%s, %s), get_course_total_reviews(%s, %s), get_course_average_rating(%s, %s)'

        tups = [dept, csn] * 6
        cursor.execute(query, tuple(tups))
        rows = [x[0] for x in cursor.description]
        data = cursor.fetchone()

        json_data = dict(zip(rows, data))
        json_dump = json.dumps(json_data)

        averages = json.loads(json_dump)
        ''' ease distribution '''
        query = "SELECT get_course_ease_distribution(%s, %s)"
        cursor.execute(query, (dept, csn))
        rows = [x[0] for x in cursor.description]

        data = cursor.fetchall()

        json_data = dict(zip(rows, data))
        json_dump = json.dumps(json_data)

        ease_dist = json.loads(json_dump)

        ''' grade distribution '''
        query = "SELECT get_course_grade_distribution(%s, %s)"
        cursor.execute(query, (dept, csn))
        rows = [x[0] for x in cursor.description]

        data = cursor.fetchall()

        json_data = dict(zip(rows, data))
        json_dump = json.dumps(json_data)

        grade_dist = json.loads(json_dump)

        final_json = row_merge([averages, ease_dist, grade_dist])

    return final_json

@api_view(['POST'])
def post_review(request):
    json_data = request.body.decode('utf-8')
    data = json.loads(json_data)
    print(data['tags'])
    return JsonResponse({"message":"something happened"})
# @api_view(['GET'])
# def courses(request):
#     if request.method == 'GET':
#         all_courses = Courses.objects.all()

#         course_serializer = CourseSerialized(all_courses, many=True)
#         return JsonResponse(course_serializer.data, safe=False)


# @api_view(['GET'])
# def course(request, csn, dept):
#     try:
#         one_course = Courses.objects.get(
#             course_number=csn, department=dept)
#     except Courses.DoesNotExist:
#         return JsonResponse({"message": "This course doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         # courseNumber = request.query_params.get('csn', None)
#         # dept = request.query_params.get('dept', None)

#         course_serializer = CourseSerialized(one_course)
#         return JsonResponse(course_serializer.data, safe=False)


# @api_view(['GET'])
# def schedule(request, csn, dept):
#     try:
#         schedule_list = Schedules.objects.get(
#             course_number=csn, department=dept)
#     except Schedules.DoesNotExist:
#         return JsonResponse({"message": "This course is not featured in our schedules"}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':

#         schedule_serializer = SchedulesSerialized(schedule_list)
#         return JsonResponse(schedule_serializer.data, safe=False)


# @api_view(['GET'])
# def coursereviews(request, csn, dept):
#     try:
#         reviews = Reviews.objects.filter(
#             course_number=csn, department=dept)
#     except Reviews.DoesNotExist:
#         return JsonResponse({"message": "There are currently no reviews for this course"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         reviews_serialized = ReviewCommentsSerialized(reviews, many=True)

#         return JsonResponse(reviews_serialized.data, status=status.HTTP_200_OK, safe=False)
