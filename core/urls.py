from django.urls import path, include
from . import views

urlpatterns = [
    path("api/auth/", include("authentication.urls")),
    # path("", views.index, name="index"),
    ##### SEARCH ENDPOINTS ########
    # path("courses/search/", views.course_search),
    # path("courses/<str:course>/", views.sql_courses),
    # path('courses/<str:course>/reviews/', views.sql_reviews),
    # path('courses/<str:course>/reviews-stats/', views.review_stats),
    # path('courses/<str:course>/summary/', views.course_summary_controller),
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
    path("professors/<str:professor_id>/schedules/", views.professor_schedules_view),
    #     path("professors/search/", views.prof_search),
    #     path("professors/<str:professor_id>/", views.sql_professors),
    #     path("professors/<str:professor_id>/reviews/", views.prof_reviews),
    #     path('professors/<str:professor_id>/schedules/',
    #          views.professor_sql_schedules),
    #     path('professors/<str:professor_id>/summary/', views.prof_summary),
    #     path('professors/<str:professor_id>/review-stats/', views.prof_review_stats),
    #     ############## schedule search ####################
    #     path('schedules/search/', views.schedule_search)
]
