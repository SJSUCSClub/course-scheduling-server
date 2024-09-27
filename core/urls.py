from django.urls import path, include
from . import views

urlpatterns = [
    path("api/auth", include("authentication.urls")),
    ##### HEALTH ENDPOINT ####
    path("health", views.health_check, name="health"),
    # path("", views.index, name="index"),
    ##### SEARCH ENDPOINTS ########
    path("courses/search", views.course_search_view),
    path(
        "courses/<str:department>-<str:course_number>/summary",
        views.course_summary_view,
    ),
    path(
        "courses/<str:department>-<str:course_number>/reviews-stats",
        views.course_reviews_stats_view,
    ),
    path(
        "courses/<str:department>-<str:course_number>/schedules",
        views.course_schedules_view,
    ),
    path(
        "courses/<str:department>-<str:course_number>/reviews",
        views.course_reviews_view,
    ),
    #     path('courses/<str:course>/reviews/comments', views.review_comments),
    #     ############### professor paths ###################
    path("professors/<str:professor_id>/summary", views.professor_summary_view),
    path("professors/<str:professor_id>/schedules", views.professor_schedules_view),
    path(
        "professors/<str:professor_id>/reviews-stats",
        views.professor_reviews_stats_view,
    ),
    path("professors/<str:professor_id>/reviews", views.professor_reviews_view),
    path("professors/search", views.professor_search_view),
    #     ############## schedule search ####################
    path("schedules/search", views.schedule_search_view),
]
