from rest_framework.decorators import api_view, permission_classes
from authentication.permissions import AuthenticatedPermission
from django.http import JsonResponse
from core.daos.utils import insert, delete, update, get
from .utils import try_response, validate_body, validate_user, format_tags
from core.services.users import (
    get_user_profile,
    get_existing_review,
    insert_review,
    update_review,
    insert_comment,
    update_comment,
    insert_flag,
    update_flag,
    insert_vote,
    update_vote
)

@api_view(["GET"])
@permission_classes([AuthenticatedPermission])
@try_response
def user_profile(request):
    json_data = get_user_profile(
        user_id = validate_user(request)
    )
    return JsonResponse(json_data, safe=False)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
@try_response
def post_review(request):
    user_id = validate_user(request)
    data = validate_body(request)
    existing_review = get_existing_review(user_id, data)
    if existing_review:
        return JsonResponse({"message": "You have already posted a review for this course professor pair."}, status=400)
    results = insert_review(user_id, data)
    return JsonResponse(results, safe=False)

def put_review(request, review_id):
    user_id = validate_user(request)
    data = validate_body(request)
    results = update_review(user_id, review_id, data)
    return JsonResponse(results, safe=False)


def delete_review(request, review_id):
    user_id = validate_user(request)
    results = delete("reviews", {"user_id": user_id, "id": review_id})
    return JsonResponse(results, safe=False)


@api_view(["PUT", "DELETE"])
@permission_classes([AuthenticatedPermission])
@try_response
def review_query(request, review_id):
    print(request.method)
    if request.method == "PUT":
        return put_review(request, review_id)
    elif request.method == "DELETE":
        return delete_review(request, review_id)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
@try_response
def post_comment(request):
    user_id = validate_user(request)
    data = validate_body(request)
    results = insert_comment(user_id,data)
    return JsonResponse(results, safe=False)


def put_comment(request):
    review_id = request.GET.get("review_id")
    comment_id = request.GET.get("comment_id")
    user_id = validate_user(request)
    data = validate_body(request)
    results = update_comment(user_id,comment_id,review_id,data)
    return JsonResponse(results, safe=False)


def delete_comment(request):
    review_id = request.GET.get("review_id")
    comment_id = request.GET.get("comment_id")
    user_id = validate_user(request)
    results = delete(
        "comments", {"user_id": user_id, "review_id": review_id, "id": comment_id}
    )
    return JsonResponse(results, safe=False)


@api_view(["PUT", "DELETE"])
@permission_classes([AuthenticatedPermission])
@try_response
def comment_query(request):
    if request.method == "PUT":
        return put_comment(request)
    elif request.method == "DELETE":
        return delete_comment(request)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
@try_response
def post_flagged_review(request):
    user_id = validate_user(request)
    data = validate_body(request)
    results = insert_flag(user_id,data)
    return JsonResponse(results, safe=False)


def put_flag(request):
    review_id = request.GET.get("review_id")
    flag_id = request.GET.get("flag_id")
    user_id = validate_user(request)
    data = validate_body(request)
    results = update_flag(user_id, flag_id, review_id, data)
    return JsonResponse(results, safe=False)


def delete_flag(request):
    review_id = request.GET.get("review_id")
    flag_id = request.GET.get("flag_id")
    user_id = validate_user(request)
    results = delete(
        "flag_reviews", {"user_id": user_id, "review_id": review_id, "id": flag_id}
    )
    return JsonResponse(results, safe=False)


@api_view(["PUT", "DELETE"])
@permission_classes([AuthenticatedPermission])
@try_response
def flagged_query(request):
    if request.method == "PUT":
        return put_flag(request)
    elif request.method == "DELETE":
        return delete_flag(request)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
@try_response
def post_vote(request):
    user_id = validate_user(request)
    data = validate_body(request)
    results = insert_vote(user_id,data)
    return JsonResponse(results, safe=False)


def put_vote(request):
    review_id = request.GET.get("review_id")
    user_id = validate_user(request)
    data = validate_body(request)
    results = update_vote(user_id,review_id,data)
    return JsonResponse(results, safe=False)


def delete_vote(request):
    review_id = request.GET.get("review_id")
    user_id = validate_user(request)
    results = delete(
        "user_review_critique", {"user_id": user_id, "review_id": review_id}
    )
    return JsonResponse(results, safe=False)


@api_view(["PUT", "DELETE"])
@permission_classes([AuthenticatedPermission])
@try_response
def vote_query(request):
    if request.method == "PUT":
        return put_vote(request)
    elif request.method == "DELETE":
        return delete_vote(request)
