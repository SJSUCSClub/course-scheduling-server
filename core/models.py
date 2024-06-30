# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

A_plus = 'A+'
A_grade = 'A'
A_min = 'A-'
B_plus = 'B+'
B_grade = 'B'
B_min = 'B-'
C_plus = 'C+'
C_grade = 'C'
C_min = 'C-'
D_plus = 'D+'
D_grade = 'D'
D_min = 'D-'
Fail = 'F'

GRADE_ENUMS = [
    (A_plus, "A+"),
    (A_grade, "A"),
    (A_min, "A-"),
    (B_plus, "B+"),
    (B_grade, "B"),
    (B_min, "B-"),
    (C_plus, "C+"),
    (C_grade, "C"),
    (C_min, "C-"),
    (D_plus, "D+"),
    (D_grade, "D"),
    (D_min, "D-"),
    (Fail, "F"),
]

TAG_ENUMS = [
    (1, "Easy grader"),
    (2, "Lots of assignments"),
    (3, "Tough grader"),
    (4, "Funny"),
]


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    email = models.TextField(unique=True)
    is_professor = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'users'


class Departments(models.Model):
    abbr_dept = models.TextField(primary_key=True)
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'departments'


class Courses(models.Model):
    # The composite primary key (course_number, department) found, that is not supported. The first column is selected.
    course_number = models.TextField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    prereqs = models.TextField(blank=True, null=True)
    units = models.TextField(blank=True, null=True)
    satisfies_area = models.TextField(blank=True, null=True)
    department = models.ForeignKey(
        Departments, models.DO_NOTHING, db_column='department')

    class Meta:
        managed = False
        db_table = 'courses'
        unique_together = (('course_number', 'department'),)


class Reviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        Users, models.CASCADE, related_name='reviews_user_id')
    professor = models.ForeignKey(
        Users, models.DO_NOTHING, related_name='reviews_professor_id')
    course_number = models.ForeignKey(
        Courses, models.DO_NOTHING, db_column='course_number')
    department = models.ForeignKey(
        Departments, models.DO_NOTHING, db_column='department')
    content = models.TextField()
    quality = models.IntegerField(
        default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    difficulty = models.IntegerField(
        default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    # This field type is a guess.
    grade = models.TextField(max_length=2, blank=True,
                             null=True, choices=GRADE_ENUMS)
    # This field type is a guess.
    tags = models.TextField(blank=True, null=True, choices=TAG_ENUMS)
    take_again = models.BooleanField()
    is_user_anonymous = models.BooleanField(
        default=False, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'


class Schedules(models.Model):
    class_number = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    course_number = models.ForeignKey(
        Courses, models.DO_NOTHING, db_column='course_number')
    section = models.TextField()
    days = models.TextField()
    dates = models.TextField()
    times = models.TextField()
    class_type = models.TextField()
    course_title = models.TextField()
    available_seats = models.IntegerField(blank=True, null=True)
    units = models.IntegerField()
    location = models.TextField(blank=True, null=True)
    mode_of_instruction = models.TextField()
    satisfies_area = models.TextField(blank=True, null=True)
    professor = models.ForeignKey(
        Users, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey(
        Departments, models.DO_NOTHING, db_column='department')

    class Meta:
        managed = False
        db_table = 'schedules'


class ProfessorCourse(models.Model):
    # The composite primary key (professor_id, course_number, department) found, that is not supported. The first column is selected.
    professor = models.OneToOneField(
        Users, models.DO_NOTHING)
    course_number = models.ForeignKey(
        Courses, models.DO_NOTHING, related_name='professor_course_number', db_column='course_number')
    department = models.ForeignKey(
        Courses, models.DO_NOTHING, related_name='professor_course_department', db_column='department')

    class Meta:
        managed = False
        db_table = 'professor_course'
        unique_together = (('professor', 'course_number', 'department'),)


class Comments(models.Model):
    cid = models.BigAutoField(primary_key=True)
    review = models.ForeignKey(Reviews, models.CASCADE)
    user = models.ForeignKey(Users, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'comments'


class FlagReviews(models.Model):
    fid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Users, models.CASCADE)
    review = models.ForeignKey(Reviews, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    class Meta:
        managed = False
        db_table = 'flag_reviews'


class UserReviewCritique(models.Model):
    # The composite primary key (user_id, review_id) found, that is not supported. The first column is selected.
    user = models.OneToOneField(Users, models.CASCADE)
    review = models.ForeignKey(
        Reviews, models.CASCADE, related_name='review_id_critique')
    upvote = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'user_review_critique'
        unique_together = (('user', 'review'),)


class Majors(models.Model):
    created_at = models.DateTimeField()
    major_name = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'majors'


class MajorRequirements(models.Model):
    # The composite primary key (id, major_name, department, course_number) found, that is not supported. The first column is selected.
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    major_name = models.ForeignKey(
        'Majors', models.DO_NOTHING, db_column='major_name')
    department = models.ForeignKey(
        Courses, models.DO_NOTHING, db_column='department')
    course_number = models.ForeignKey(
        Courses, models.DO_NOTHING, related_name='major_requirements_course_number', db_column='course_number')

    class Meta:
        managed = False
        db_table = 'major_requirements'
        unique_together = (
            ('id', 'major_name', 'department', 'course_number'),)
