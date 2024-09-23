from rest_framework.decorators import api_view, permission_classes
from authentication.permissions import AuthenticatedPermission
from django.http import JsonResponse


@api_view(["GET"])
@permission_classes([AuthenticatedPermission])
def user_profile(request):
    try:
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

    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
def post_review(request):
    try:
        user_id = request.user.email[0:-9]
        print(user_id)
        json_data = request.body.decode("utf-8")
        data = json.loads(json_data)
        results = insert(
            "reviews",
            {
                "user_id": user_id,
                "professor_id": data["professor_id"],
                "course_number": data["course_number"],
                "department": data["department"],
                "content": data["content"],
                "quality": data["quality"],
                "ease": data["ease"],
                "grade": data["grade"],
                "take_again": data["take_again"],
                "tags": data["tags"],
                "is_user_anonymous": data["is_user_anonymous"],
            },
        )
        return JsonResponse(results, safe=False)
    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)


def put_review(request, review_id):
    user_id = request.user.email[0:-9]
    json_data = request.body.decode("utf-8")
    data = json.loads(json_data)
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
    user_id = request.user.email[0:-9]
    results = delete("reviews", {"user_id": user_id, "id": review_id})
    return JsonResponse(results, safe=False)


@api_view(["PUT", "DELETE"])
@permission_classes([AuthenticatedPermission])
def review_query(request, review_id):
    try:
        print(request.method)
        if request.method == "PUT":
            return put_review(request, review_id)
        elif request.method == "DELETE":
            return delete_review(request, review_id)
    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
def post_comment(request):
    try:
        user_id = request.user.email[0:-9]
        json_data = request.body.decode("utf-8")
        data = json.loads(json_data)
        results = insert(
            "comments",
            {
                "user_id": user_id,
                "review_id": data["review_id"],
                "content": data["content"],
            },
        )
        return JsonResponse(results, safe=False)
    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)


def put_comment(request):
    review_id = request.GET.get("review_id")
    comment_id = request.GET.get("comment_id")
    user_id = request.user.email[0:-9]
    json_data = request.body.decode("utf-8")
    data = json.loads(json_data)
    results = update(
        "comments",
        {"content": data["content"], "updated_at": datetime.now()},
        {"user_id": user_id, "review_id": review_id, "id": comment_id},
    )
    return JsonResponse(results, safe=False)


def delete_comment(request):
    review_id = request.GET.get("review_id")
    comment_id = request.GET.get("comment_id")
    user_id = request.user.email[0:-9]
    results = delete(
        "comments", {"user_id": user_id, "review_id": review_id, "id": comment_id}
    )
    return JsonResponse(results, safe=False)


@api_view(["PUT", "DELETE"])
@permission_classes([AuthenticatedPermission])
def comment_query(request):
    try:
        if request.method == "PUT":
            return put_comment(request)
        elif request.method == "DELETE":
            return delete_comment(request)
    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
def post_flagged_review(request):
    try:
        user_id = request.user.email[0:-9]
        json_data = request.body.decode("utf-8")
        data = json.loads(json_data)
        results = insert(
            "flag_reviews",
            {
                "user_id": user_id,
                "review_id": data["review_id"],
                "reason": data["reason"],
            },
        )
        return JsonResponse(results, safe=False)
    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)


def put_flag(request):
    review_id = request.GET.get("review_id")
    flag_id = request.GET.get("flag_id")
    user_id = request.user.email[0:-9]
    json_data = request.body.decode("utf-8")
    data = json.loads(json_data)
    results = update(
        "flag_reviews",
        {"reason": data["reason"]},
        {"user_id": user_id, "review_id": review_id, "id": flag_id},
    )
    return JsonResponse(results, safe=False)


def delete_flag(request):
    review_id = request.GET.get("review_id")
    flag_id = request.GET.get("flag_id")
    user_id = request.user.email[0:-9]
    results = delete(
        "flag_reviews", {"user_id": user_id, "review_id": review_id, "id": flag_id}
    )
    return JsonResponse(results, safe=False)


@api_view(["PUT", "DELETE"])
@permission_classes([AuthenticatedPermission])
def flagged_query(request):
    try:
        if request.method == "PUT":
            return put_flag(request)
        elif request.method == "DELETE":
            return delete_flag(request)
    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)


@api_view(["POST"])
@permission_classes([AuthenticatedPermission])
def post_vote(request):
    # try:
    user_id = request.user.email[0:-9]
    json_data = request.body.decode("utf-8")
    data = json.loads(json_data)
    results = insert(
        "user_review_critique",
        {"user_id": user_id, "review_id": data["review_id"], "upvote": data["vote"]},
    )
    return JsonResponse(results, safe=False)


# except:
#     return JsonResponse({"message": "Internal Server Error"}, status=500)


def put_vote(request):
    review_id = request.GET.get("review_id")
    user_id = request.user.email[0:-9]
    json_data = request.body.decode("utf-8")
    data = json.loads(json_data)
    results = update(
        "user_review_critique",
        {"upvote": data["vote"]},
        {"user_id": user_id, "review_id": review_id},
    )
    return JsonResponse(results, safe=False)


def delete_vote(request):
    review_id = request.GET.get("review_id")
    user_id = request.user.email[0:-9]
    results = delete(
        "user_review_critique", {"user_id": user_id, "review_id": review_id}
    )
    return JsonResponse(results, safe=False)


@api_view(["PUT", "DELETE"])
@permission_classes([AuthenticatedPermission])
def vote_query(request):
    try:
        if request.method == "PUT":
            return put_vote(request)
        elif request.method == "DELETE":
            return delete_vote(request)
    except:
        return JsonResponse({"message": "Internal Server Error"}, status=500)
