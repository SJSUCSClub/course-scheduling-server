from django.urls import path, include
from . import views

urlpatterns = [
    path("api/auth/", include("authentication.urls")),
    # path("", views.index, name="index"),
    ##### SEARCH ENDPOINTS ########
    # path("courses/search/", views.course_search),
    path(
        "courses/<str:department>/<str:course_number>/summary/",
        views.courses.course_summary_view,
    ),
    path(
        "courses/<str:department>/<str:course_number>/reviews-stats/",
        views.courses.course_reviews_stats_view,
    ),
    path(
        "courses/<str:department>/<str:course_number>/schedules/",
        views.courses.course_schedules_view,
    ),
    path(
        "courses/<str:department>/<str:course_number>/reviews/",
        views.courses.course_reviews_view,
    ),
    #     path('courses/<str:course>/reviews/comments', views.review_comments),
    #     path('courses/<str:course>/schedules/', views.sql_schedules),
    #     ############### professor paths ###################
    path("professors/<str:professor_id>/summary/", views.professor_summary_view),
    path("professors/<str:professor_id>/schedules/", views.professor_schedules_view),
    path(
        "professors/<str:professor_id>/reviews-stats/",
        views.professor_reviews_stats_view,
    ),
    path("professors/<str:professor_id>/reviews/", views.professor_reviews_view),
    #     path("professors/search/", views.prof_search),
    #     ############## schedule search ####################
    #     path('schedules/search/', views.schedule_search)
]
