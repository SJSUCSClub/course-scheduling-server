from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("courses/", views.sql_courses),
    path('courses/reviews/', views.sql_reviews),
    path('courses/review_stats/', views.review_stats),
    path('courses/summary/', views.summary),
    path('courses/reviews/comments', views.review_comments),
    path('courses/schedules/', views.sql_schedules),

    path("users/profile", views.user_profile),

    path('users/reviews',views.post_review),
    path('users/comments',views.post_comment),
    path('users/flagged_reviews',views.post_flagged_review),
    path('users/vote',views.post_vote),

    path('users/reviews/<int:review_id>',views.review_query),
    path('users/reviews/comments/',views.comment_query),
    path('users/reviews/flagged_reviews/',views.flagged_query),
    path('users/reviews/vote/',views.vote_query),
    # path("", views.index, name="index"),
    ##### SEARCH ENDPOINTS ########
    path("courses/search/", views.course_search),
    path("courses/<str:course>/", views.sql_courses),
    path('courses/<str:course>/reviews/', views.sql_reviews),
    path('courses/<str:course>/review-stats/', views.review_stats),
    path('courses/<str:course>/summary/', views.summary),
    path('courses/<str:course>/reviews/comments', views.review_comments),
    path('courses/<str:course>/schedules/', views.sql_schedules),
    ############### professor paths ###################
    path("professors/search/", views.prof_search),
    path("professors/<str:professor_id>/", views.sql_professors),
    path("professors/<str:professor_id>/reviews/", views.prof_reviews),
    path('professors/<str:professor_id>/schedules/',
         views.professor_sql_schedules),
    path('professors/<str:professor_id>/summary/', views.prof_summary),
    path('professors/<str:professor_id>/review-stats/', views.prof_review_stats),
    ############## schedule search ####################
    path('schedules/search/', views.schedule_search)
]
