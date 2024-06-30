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

]
