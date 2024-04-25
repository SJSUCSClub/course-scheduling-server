from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('api/auth/', include('authentication.urls')),
    path("", views.index, name="index"),
    path("courses/", views.sql_courses),
    path('courses/reviews/', views.sql_reviews),
    path('courses/review_stats/', views.review_stats),
    path('courses/summary/', views.summary),
    path('courses/reviews/comments', views.review_comments),
    path('courses/schedules/', views.sql_schedules),

    path('users/reviews',views.post_review),
    path('users/comments',views.post_comment),
    path('users/flagged_reviews',views.post_flagged_review),
    path('users/vote',views.post_vote)

    
]
