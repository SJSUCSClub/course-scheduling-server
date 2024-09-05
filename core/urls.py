from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('api/auth/', include('authentication.urls')),
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
