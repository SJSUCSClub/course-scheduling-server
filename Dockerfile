FROM python:3.12

WORKDIR /app

# install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project files
COPY authentication/ authentication/
COPY core/ core/
COPY course_scheduling/ course_scheduling/
COPY manage.py manage.py
COPY client_secret.json client_secret.json

# set environment variables
# (these get re-set by the compose, but they're here for reference)
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_HOST=0.0.0.0
ENV DB_PORT=5432

# expose port
EXPOSE 8000

# run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]