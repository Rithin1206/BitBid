FROM python:slim

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
ENV PROD 1

COPY bitbid_project/ ./
COPY requirements.txt ./
RUN pip install -r requirements.txt

# run db migrations
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py migrate --run-syncdb 

# collect static files
RUN python manage.py collectstatic --noinput

# CMD ["python", "manage.py", "runserver", "0.0.0.0:$PORT"]
CMD gunicorn bitbid_project.wsgi:application --bind 0.0.0.0:$PORT