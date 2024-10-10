from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from core.daos import departments_select_all
from .utils import try_response


@api_view(["GET"])
@try_response
def departments_view(request):
    return JsonResponse({"departments": departments_select_all()})
