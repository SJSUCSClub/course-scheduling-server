from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('api/auth/', include('authentication.urls')),
    path("", views.index, name="index"),
    path("courses/", views.sql_courses),
    path('courses/<str:csn>/<str:dept>/', views.course),
    path('courses/reviews/<str:csn>/<str:dept>/', views.coursereviews),
    path('courses/schedules/', views.sql_schedules)
]
