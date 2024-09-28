from rest_framework.decorators import api_view, permission_classes
from authentication.permissions import AuthenticatedPermission
from django.http import JsonResponse
from core.daos.utils import insert, delete, update
from .utils import try_response, validate_body, validate_user
from datetime import datetime


@api_view(["GET"])
@permission_classes([AuthenticatedPermission])
@try_response
def user_profile(request):
    result = {}
    user_id = request.user.email[0:-9]
    reviews = where("reviews", {"user_id": user_id})
    for i in range(len(reviews)):
        current_review = reviews[i]
        comments = where("Comments", {"review_id": current_review["id"]})
        current_review["comments"] = comments
        voted = where(
            "user_review_critique",
            {"user_id": user_id, "review_id": current_review["id"]},
            ["user_review_critique"],
        )
        current_review["voted"] = voted[0]["vote"] if len(voted) > 0 else None

        votes = calculate_votes(
            "user_review_critique",
            {"user_id": user_id, "review_id": current_review["id"]},
        )[0][0]
        votes_dict = {}
        votes_dict["upvotes"] = votes[0]
        votes_dict["downvotes"] = votes[1]
        current_review["votes"] = votes_dict

    result["review"] = reviews
    comments = where("Comments", {"user_id": user_id})
    result["comments"] = comments
    flagged = where("flag_reviews", {"user_id": user_id})
    result["flagged_reviews"] = flagged
    voted = where("user_review_critique", {"user_id": user_id})
    result["reviews_voted"] = voted

    return JsonResponse(result, safe=False)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
@try_response
def post_review(request):
    user_id = validate_user(request)
    data = validate_body(request)
    insert(**data, user_id=user_id)
    return JsonResponse({})


def put_review(request, review_id):
    user_id = validate_user(request)
    data = validate_body(request)
    results = update(
        "reviews",
        {
            "content": data["content"],
            "quality": data["quality"],
            "ease": data["ease"],
            "grade": data["grade"],
            "take_again": data["take_again"],
            "tags": data["tags"],
            "is_user_anonymous": data["is_user_anonymous"],
        },
        {"user_id": user_id, "id": review_id},
    )
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
    results = insert(
        "comments",
        {
            "user_id": user_id,
            "review_id": data["review_id"],
            "content": data["content"],
        },
    )
    return JsonResponse(results, safe=False)


def put_comment(request):
    review_id = request.GET.get("review_id")
    comment_id = request.GET.get("comment_id")
    user_id = validate_user(request)
    data = validate_body(request)
    results = update(
        "comments",
        {"content": data["content"], "updated_at": datetime.now()},
        {"user_id": user_id, "review_id": review_id, "id": comment_id},
    )
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
    results = insert(
        "flag_reviews",
        {
            "user_id": user_id,
            "review_id": data["review_id"],
            "reason": data["reason"],
        },
    )
    return JsonResponse(results, safe=False)


def put_flag(request):
    review_id = request.GET.get("review_id")
    flag_id = request.GET.get("flag_id")
    user_id = validate_user(request)
    data = validate_body(request)
    results = update(
        "flag_reviews",
        {"reason": data["reason"]},
        {"user_id": user_id, "review_id": review_id, "id": flag_id},
    )
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
    # try:
    user_id = validate_user(request)
    data = validate_body(request)
    results = insert(
        "user_review_critique",
        {"user_id": user_id, "review_id": data["review_id"], "upvote": data["vote"]},
    )
    return JsonResponse(results, safe=False)


def put_vote(request):
    review_id = request.GET.get("review_id")
    user_id = validate_user(request)
    data = validate_body(request)
    results = update(
        "user_review_critique",
        {"upvote": data["vote"]},
        {"user_id": user_id, "review_id": review_id},
    )
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
