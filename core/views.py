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
import re


def pull_reviews(csn, dept, comments, page=None, limit=None, tags=None):

    if page:
        page = int(page)
        if limit:
            limit = int(limit)
        else:
            limit = 10
    else:
        page = 1
        limit = 10
    json_data = where(
        'Reviews', {'course_number': csn, 'department': dept}, page=page,
        limit=limit, tags=tags
    )

    init_json = where(
        'Reviews', {'course_number': csn, 'department': dept}, tags=tags)

    final_arr = []
    unique_tags = set()
    res = dict()
    res['total_reviews'] = len(init_json)
    for json_obj in init_json:
        if json_obj['tags']:
            temp = str(json_obj['tags'])
            temp = temp.replace('\\', '')
            temp = temp.replace('"', '')
            temp = temp.replace('{', '')
            temp = temp.replace('}', '')
            temp = temp.split(',')

            for t in temp:
                unique_tags.add(t)

    for json_obj in json_data:
        ''' replace tag string with array and save unique tags '''
        if json_obj['tags']:
            temp = str(json_obj['tags'])
            temp = temp.replace('\\', '')
            temp = temp.replace('"', '')
            temp = temp.replace('{', '')
            temp = temp.replace('}', '')
            # print(temp)
            temp = temp.split(',')
            json_obj['tags'] = temp

        ''' Get review critics '''
        if json_obj['id'] is not None:
            critiques = {'upvote': 0, 'downvote': 0}

            critics = where('user_review_critique', {
                            'review_id': json_obj['id']}, ['upvote'])
            for critic in critics:
                if critic['upvote'] == True:
                    critiques['upvote'] += 1
                else:
                    critiques['downvote'] += 1

            if comments and comments != False and comments.capitalize() != "False" and comments.capitalize() == "True":
                comments = where('comments', {
                    'review_id': json_obj['id']})
                json_obj = row_merge(
                    [json_obj, {'critics': critiques}, {'comments': comments}])
            else:
                json_obj = row_merge([json_obj, {'critics': critiques}])

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
    filter_results = dict()
    if len(init_json) < limit:
        filter_results['pages'] = 1
    else:
        filter_results['pages'] = len(init_json) // (
            int(limit) if not None else 10)
    filter_results['tags'] = list(unique_tags)
    res['filters'] = filter_results
    res['reviews'] = final_arr

    return res


@api_view(['GET'])
def sql_courses(request, course):
    try:
        course = course.split('-')
        csn = course[-1]
        dept = course[0]

        if csn and dept:
            json_data = where(
                'Courses', {'course_number': csn, 'department': dept})
            if len(json_data) > 0:
                json_data[0]['reviews'] = pull_reviews(csn, dept, False)

        else:
            json_data = general_statements('Courses')

        return JsonResponse(json_data, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


@api_view(['GET'])
def sql_schedules(request, course):
    try:
        course = course.split('-')
        csn = course[-1]
        dept = course[0]

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

        return JsonResponse(final_arr, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


@api_view(['GET'])
def sql_reviews(request, course):
    try:
        course = course.split('-')
        csn = course[-1]
        dept = course[0]

        page = request.GET.get('page')
        limit = request.GET.get('limit')
        tags = request.GET.getlist('tags')

        comments = request.GET.get('comments')

        final_arr = pull_reviews(csn, dept, comments, page, limit, tags)

        return JsonResponse(final_arr, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


@api_view(['GET'])
def review_stats(request, course):
    try:
        course = course.split('-')
        csn = course[-1]
        dept = course[0]

        if csn is not None and dept is not None:

            final_json = auxiliary_json(dept, csn)
            return JsonResponse(final_json, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


@api_view(['GET'])
def summary(request, course):
    try:
        course = course.split('-')
        csn = course[-1]
        dept = course[0]
        if csn is not None and dept is not None:
            json_data = where(
                'Courses', {'course_number': csn, 'department': dept})

            # print(json_data)
            if len(json_data) > 0:
                partial_json = auxiliary_json(dept, csn)
                finalized_json = row_merge([json_data[0], partial_json])

                return JsonResponse(finalized_json, safe=False)
            else:
                return JsonResponse({"message": "Specified course not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return JsonResponse({"message": " course_number and or department not specified"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


''' In the event we need to pull all the comments pertaining to a certain course'''


@api_view(['GET'])
def review_comments(request, course):
    try:
        course = course.split('-')
        csn = course[-1]
        dept = course[0]

        if csn is not None and dept is not None:
            review_ids = where(
                'Reviews', {'course_number': csn, 'department': dept}, ['id'])

            total_comments = []
            for id in review_ids:
                comments = where('Comments', {'review_id': id})
                total_comments += comments

            return JsonResponse(total_comments, safe=False)

        return JsonResponse({"message": " course_number and or department not specified"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


def auxiliary_json(dept, csn):
    with connection.cursor() as cursor:
        ''' Initial averages '''
        query = 'SELECT get_course_average_grade(%s, %s) as avg_grade, get_course_average_quality(%s, %s) as avg_quality, get_course_average_ease(%s, %s) as avg_ease,get_course_take_again_percent(%s, %s) as take_again_percent, get_course_total_reviews(%s, %s) as total_reviews, get_course_average_rating(%s, %s) as avg_rating'

        tups = [dept, csn] * 6
        cursor.execute(query, tuple(tups))
        rows = [x[0] for x in cursor.description]
        data = cursor.fetchone()

        json_data = dict(zip(rows, data))
        json_dump = json.dumps(json_data)

        averages = json.loads(json_dump)
        ''' ease distribution '''
        query = "SELECT get_course_ease_distribution(%s, %s) as ease_distribution"
        ease_dist = query_execution(query, (dept, csn))
        ease_dist['ease_distribution'] = string_to_list_int(
            ease_dist, 'ease_distribution')

        ''' grade distribution '''
        query = "SELECT get_course_grade_distribution(%s, %s) as grade_distibution"
        grade_dist = query_execution(query, (dept, csn))
        grade_dist['grade_distibution'] = string_to_list_int(
            grade_dist, 'grade_distibution')

        ''' quality distribution '''
        query = "SELECT get_course_quality_distribution(%s, %s) as quality_distribution"
        quality_dist = query_execution(query, (dept, csn))
        quality_dist['quality_distribution'] = string_to_list_int(
            quality_dist, 'quality_distribution')

        ''' rating distribution '''
        query = "SELECT get_course_rating_distribution(%s, %s) as rating_distribution"
        rating_dist = query_execution(query, (dept, csn))
        rating_dist['rating_distribution'] = string_to_list_int(
            rating_dist, 'rating_distribution')

        final_json = row_merge(
            [averages, ease_dist, grade_dist, quality_dist, rating_dist])

    final_json['course number'] = csn
    final_json['department'] = dept
    return final_json


''' 
    params: 
        diction - json obj / dictionary
        key - specific key containing list
    converts the values to a list of 
    comma separated integers
    returns list of ints
'''


def string_to_list_int(diction, key):
    grades = diction[key][0].split(',')
    grades = [int(re.sub("[^0-9]", "", x)) for x in grades]
    return grades


def query_execution(query, params: tuple):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = [x[0] for x in cursor.description]

        data = cursor.fetchall()

        json_data = dict(zip(rows, data))
        json_dump = json.dumps(json_data)
        results = json.loads(json_dump)
    return results


########################################################################
########################################################################
########################################################################
###################### PROFESSOR ENDPOINTS #############################


def prof_auxiliary_json(prof_id):
    with connection.cursor() as cursor:
        ''' Initial averages '''
        query = 'SELECT get_professor_average_grade(%s) as avg_grade, get_professor_average_quality(%s) as avg_quality, get_professor_average_ease(%s) as avg_ease,get_professor_take_again_percent(%s) as take_again_percent, get_professor_total_reviews(%s) as total_reviews, get_professor_average_rating(%s) as avg_rating'

        tups = [prof_id] * 6
        cursor.execute(query, tuple(tups))
        rows = [x[0] for x in cursor.description]
        data = cursor.fetchone()

        json_data = dict(zip(rows, data))
        json_dump = json.dumps(json_data)

        averages = json.loads(json_dump)
        ''' ease distribution '''
        query = "SELECT get_professor_ease_distribution(%s) as ease_distribution"
        ease_dist = query_execution(query, (prof_id,))
        ease_dist['ease_distribution'] = string_to_list_int(
            ease_dist, 'ease_distribution')

        ''' grade distribution '''
        query = "SELECT get_professor_grade_distribution(%s) as grade_distribution"
        grade_dist = query_execution(query, (prof_id,))
        grade_dist['grade_distribution'] = string_to_list_int(
            grade_dist, 'grade_distribution')

        ''' quality distribution '''
        query = "SELECT get_professor_quality_distribution(%s) as quality_distribution"
        quality_dist = query_execution(query, (prof_id,))
        quality_dist['quality_distribution'] = string_to_list_int(
            quality_dist, 'quality_distribution')

        ''' rating distribution '''
        query = "SELECT get_professor_rating_distribution(%s) as rating_distribution"
        rating_dist = query_execution(query, (prof_id,))
        rating_dist['rating_distribution'] = string_to_list_int(
            rating_dist, 'rating_distribution')

        final_json = row_merge(
            [averages, ease_dist, grade_dist, quality_dist, rating_dist])

    return final_json


def prof_pull_reviews(prof_id, comments, page=None, limit=None, tags=None):

    if page:
        page = int(page)
        if limit:
            limit = int(limit)
        else:
            limit = 10
    else:
        page = 1
        limit = 10

    json_data = where(
        'Reviews', {'professor_id': prof_id}, page=page,
        limit=limit, tags=tags
    )

    init_json = where(
        'Reviews', {'professor_id': prof_id}, tags=tags
    )

    final_arr = []
    unique_tags = set()
    res = dict()
    res['total_reviews'] = len(init_json)

    for json_obj in init_json:
        if json_obj['tags']:
            temp = str(json_obj['tags'])
            temp = temp.replace('\\', '')
            temp = temp.replace('"', '')
            temp = temp.replace('{', '')
            temp = temp.replace('}', '')
            temp = temp.split(',')

            for t in temp:
                unique_tags.add(t)

    for json_obj in json_data:
        ''' replace tag string with array and save unique tags '''
        if json_obj['tags']:
            temp = str(json_obj['tags'])
            temp = temp.replace('\\', '')
            temp = temp.replace('"', '')
            temp = temp.replace('{', '')
            temp = temp.replace('}', '')
            # print(temp)
            temp = temp.split(',')

            for t in temp:
                # print(t)
                unique_tags.add(t)
            json_obj['tags'] = temp

        ''' Get review critics '''
        if json_obj['id'] is not None:
            critics = where('user_review_critique', {
                            'review_id': json_obj['id']}, ['upvote'])
            if comments and comments != False and str(comments).capitalize != "False":
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

    res['pages'] = len(init_json) // (int(limit) if not None else 10)
    res['tags'] = list(unique_tags)
    res['reviews'] = final_arr

    return res


@api_view(['GET'])
def sql_professors(request, professor_id):
    try:
        prof_id = professor_id

        if prof_id:
            json_data = where(
                'users', {'id': prof_id, 'is_professor': True})
            if len(json_data) > 0:
                json_data[0]['reviews'] = prof_pull_reviews(prof_id, False)
        else:
            json_data = general_statements('users')

        return JsonResponse(json_data, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


# professor schedules
@api_view(['GET'])
def professor_sql_schedules(request, professor_id):
    try:
        prof_id = professor_id

        if prof_id is not None:
            json_data = where(
                'Schedules', {'professor_id': prof_id})

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

        if json_data is None:
            return JsonResponse({"message": "An error occurred"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(final_arr, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


@api_view(['GET'])
def prof_summary(request, professor_id):
    try:
        prof_id = professor_id

        if prof_id is not None:
            json_data = where(
                'users', {'id': prof_id})

            # print(json_data)
            if len(json_data) > 0:
                partial_json = prof_auxiliary_json(prof_id)
                if len(partial_json) > 0:
                    finalized_json = row_merge([json_data[0], partial_json])

                return JsonResponse(finalized_json, safe=False)
            else:
                return JsonResponse({"message": "Specified course not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return JsonResponse({"message": " professor_id not specified"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)

# professor review stats


@api_view(['GET'])
def prof_review_stats(request, professor_id):
    try:
        prof_id = professor_id

        if prof_id is not None:

            final_json = prof_auxiliary_json(prof_id)
            final_json['id'] = prof_id
            return JsonResponse(final_json, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)

# professor reviews


@api_view(['GET'])
def prof_reviews(request, professor_id):

    try:
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        tags = request.GET.getlist('tags')

        if page is None:
            page = 1
            limit = 10

        if limit and limit not in ['10', '20', '50']:
            limit = 10
        elif limit:
            limit = int(limit)

        comments = request.GET.get('comments')

        count_query = "select count(*) as total_count from reviews where professor_id=%s"
        count, _ = run_sql(count_query, (professor_id, ))
        count = count[0][0]
        query = """
        select users.id as user_id, reviews.id as review_id, 
            reviews.created_at, 
            reviews.updated_at, users.name, users.username, 
            reviews.course_number, reviews.department, 
            reviews.professor_id, reviews.content, reviews.quality, 
            reviews.ease, reviews.grade, reviews.tags, reviews.take_again, 
            reviews.is_user_anonymous
            from reviews left join users on users.id = reviews.user_id
        where reviews.professor_id = %s
            """

        if tags and len(tags) > 0:
            new_tags = []
            for tag in tags:
                new_tags.append("'" + tag + "'")
            tag_str = '(array[' + ','.join(new_tags) + '])::tag_enum[]'
            query += tag_str + '<@tags '

        data, rows = run_sql(query + "limit %s offset %s",
                             (professor_id, limit, page))

        json_res = dictionify(data, rows)

        final_res = dict()
        unique_tags = set()
        final_res['total_results'] = count
        for json_obj in json_res:
            ''' replace tag string with array and save unique tags '''
            if json_obj['tags']:
                temp = str(json_obj['tags'])
                temp = temp.replace('\\', '')
                temp = temp.replace('"', '')
                temp = temp.replace('{', '')
                temp = temp.replace('}', '')
                # print(temp)
                temp = temp.split(',')

                for t in temp:
                    # print(t)
                    unique_tags.add(t)
                json_obj['tags'] = temp

            ''' add upvots and downvotes'''
            if json_obj['review_id'] is not None:
                critiques = {'upvote': 0, 'downvote': 0}

                critics = where('user_review_critique', {
                                'review_id': json_obj['review_id']}, ['upvote'])
                for critic in critics:
                    if critic['upvote'] == True:
                        critiques['upvote'] += 1
                    else:
                        critiques['downvote'] += 1
                json_obj['critics'] = critiques

            ''' add comments '''
            if comments and comments.capitalize() == "True":
                comments = where('comments', {
                    'review_id': json_obj['review_id']})
                json_obj['comments'] = comments

        if count < limit:
            final_res['pages'] = 1
        else:
            final_res['pages'] = (count // (int(limit) if not None else 10)) if (count % int(
                limit) == 0) else (count // (int(limit) if not None else 10)) + 1

        filter_results = dict()
        filter_results['tags'] = list(unique_tags)
        final_res['filters'] = filter_results
        final_res['reviews'] = json_res

        return JsonResponse(final_res, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


def course_search(request):
    try:
        search = request.GET.get('search', "")
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        dept = request.GET.get('department')

        if limit and limit != 10 and limit not in ['10', '20', '50']:
            limit = 10
        elif limit and limit in ['10', '20', '50']:
            limit = int(limit)

        # if type(page) == str:
        #     page = 1

        with connection.cursor() as cursor:
            cursor.execute('SELECT set_limit(0.45)')

        query1_vars = (search, search, )
        query2_vars = (search, search, )

        query1 = """
            select * from (select *, similarity((department || ' ' || course_number), %s) AS sml from courses where (department || ' ' || course_number) %% %s
            """
        query2 = """
        union select *, similarity(name, %s) as sml from courses where name %% %s
        """

        # count_query = "SELECT COUNT(*) as total_count FROM courses WHERE name %% %s"
        # count_vars = (search, )
        if dept:
            tmp = " AND department = %s"
            query1 += tmp
            query2 += tmp
            query1_vars += (dept, )
            query2_vars += (dept, )

        end_query = ") as t order by sml desc"

        # query += """ORDER BY search_results DESC, name"""
        query = query1 + query2 + end_query
        vars = query1_vars + query2_vars
        init_query, rows = run_sql(query, vars)
        init_json = dictionify(init_query, rows)
        count = len(init_json)

        query += """ LIMIT %s OFFSET %s """

        vars += (limit, (int(page) - 1)*int(limit), )

        data, rows = run_sql(query, vars)
        json_res = dictionify(data, rows)

        unique_depts = set()
        final_results = dict()
        final_results['total_results'] = count
        for json_obj in init_json:
            unique_depts.add(json_obj['department'])

        final_results['pages'] = (
            count // limit) if count % limit == 0 else (count // limit) + 1

        filter_results = dict()
        filter_results['departments'] = list(unique_depts)
        filter_results['courses'] = json_res

        final_results['filters'] = filter_results

        return JsonResponse(final_results, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)

# professor search


def prof_search(request):
    try:
        search = request.GET.get('search', "")
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)

        if limit and limit != 10 and limit not in ['10', '20', '50']:
            limit = 10
        elif limit and limit in ['10', '20', '50']:
            limit = int(limit)

        if type(page) == str:
            page = 1

        vars = (search, search, )
        query = """
            SELECT name,email, similarity(name, %s) AS search_results
            FROM users
            WHERE name %% %s """
        count_query = "SELECT COUNT(*) as total_count FROM users WHERE name %% %s"
        count_vars = (search, )

        query += """ORDER BY search_results DESC, name"""

        count, _ = run_sql(count_query, count_vars)
        count = count[0][0]
        query += """ LIMIT %s OFFSET %s """

        vars += (limit, (int(page) - 1)*int(limit), )

        data, rows = run_sql(query, vars)
        json_res = dictionify(data, rows)

        final_results = dict()
        final_results['total_results'] = count

        final_results['pages'] = (
            count // limit) if count % limit == 0 else (count // limit) + 1
        final_results['courses'] = json_res

        return JsonResponse(final_results, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)


"""  WHY THE HELL IS THERE EVEN A SCHEDULE SEARCH FFS  """


def schedule_search(request):
    try:
        search = request.GET.get('search', "")
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        term = request.GET.get('term')
        year = request.GET.get('year')
        professor_name = request.GET.get('professor_name')
        course_number = request.GET.get('course_number')
        department = request.GET.get('department')
        moi = request.GET.get('mode_of_instruction')
        units = request.GET.getlist('units')

        if limit and limit != 10 and limit not in ['10', '20', '50']:
            limit = 10
        elif limit and limit in ['10', '20', '50']:
            limit = int(limit)

        where_cases = {'term': term, 'year': year, 'professor_name': professor_name,
                       'course_number': course_number, 'department': department, 'mode_of_instruction': moi, 'units': units}
        where_cond = " WHERE (course_dept ILIKE %s OR course_title ILIKE %s) "
        where_list = []
        new_search = "%" + search + "%"
        vars = (new_search, new_search, )

        units_check = []
        for case in where_cases.keys():
            # print(where_cases[case], case)
            if case == 'units' and len(units) > 0:
                for unit in units:
                    units_check.append(case + " = %s ")
                    vars += (unit,)
                where_list.append(f"({' OR '.join(units_check)})")
            elif where_cases[case]:
                # add where case to list of where cases
                where_list.append(case + " ILIKE %s ")
                vars += ("%" + where_cases[case] + "%",)

        if len(where_list) == 0:
            where_cond += ' AND '.join(where_list)

        sub_query = """
                SELECT s.term, s.year, s.class_number,
                s.units, s.section, s.days, s.dates, s.times,
                s.class_type, s.location, s.mode_of_instruction,
                s.professor_id, u.name as professor_name, 
                c.name as course_title, s.department, s.course_number, s.satisfies_area, CONCAT(s.department, '-', s.course_number) as course_dept FROM schedules as s LEFT JOIN users as u ON s.professor_id = u.id 
                LEFT JOIN courses as c ON s.department = c.department AND s.course_number = c.course_number
            """

        # count_query = f"SELECT COUNT(*) FROM ({sub_query}) as t"
        query = f"SELECT * FROM ({sub_query}) as t "

        # count_query += where_cond
        query += where_cond

        data, rows = run_sql(query, vars)
        init_json = dictionify(data, rows)
        # count = count[0][0]
        query += " LIMIT %s OFFSET %s"
        vars += (limit, (int(page) - 1)*int(limit), )

        data, rows = run_sql(query, vars)
        json_res = dictionify(data, rows)

        uterms, uyears, uprof_names, ucn, udept, umoi, uunits = set(
        ), set(), set(), set(), set(), set(), set()

        for json_obj in init_json:
            if json_obj['term']:
                uterms.add(json_obj['term'])
            if json_obj['year']:
                uyears.add(json_obj['year'])
            if json_obj['professor_name']:
                uprof_names.add(json_obj['professor_name'])
            if json_obj['course_number']:
                ucn.add(json_obj['course_number'])
            if json_obj['department']:
                udept.add(json_obj['department'])
            if json_obj['mode_of_instruction']:
                umoi.add(json_obj['mode_of_instruction'])
            if json_obj['units']:
                uunits.add(json_obj['units'])

        final_result = dict()
        count = len(init_json)
        final_result['total_results'] = count
        final_result['pages'] = (
            count // limit) if count % limit == 0 else (count // limit) + 1
        filter_result = dict()
        filter_result['term'] = list(uterms)
        filter_result['year'] = list(uyears)
        filter_result['professor_name'] = list(uprof_names)
        filter_result['course_number'] = list(ucn)
        filter_result['department'] = list(udept)
        filter_result['mode_of_instruction'] = list(umoi)
        filter_result['units'] = list(uunits)

        final_result['filters'] = filter_result

        final_result['schedules'] = json_res

        return JsonResponse(final_result, safe=False)
    except:
        return JsonResponse({"message": "An error occurred"}, status=500)
