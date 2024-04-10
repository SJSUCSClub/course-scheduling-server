from rest_framework import serializers
from django.db.models import QuerySet
from core.models import Users, Departments, Courses, ProfessorCourse, Reviews, Comments, Schedules


class UsersSerialized(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


class CourseSerialized(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class ReviewsSerialized(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class CommentsSerialized(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class SchedulesSerialized(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'


class ReviewCommentsSerialized(serializers.ModelSerializer):
    comments = CommentsSerialized(many=True, read_only=True)

    class Meta:
        model = Reviews
        fields = ['id', 'created_at', 'user_id', 'professor_id', 'course_number', 'department', 'content',
                  'quality', 'difficulty', 'grade', 'tags', 'take_again', 'is_user_anonymous', 'comments']
