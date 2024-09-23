from django.db import connection


def users_insert(name: str, id: str, email: str, is_professor: bool):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, id, email, is_professor, username) VALUES (%s, %s, %s, %s, generateUsername())",
            (name, id, email, is_professor),
        )
