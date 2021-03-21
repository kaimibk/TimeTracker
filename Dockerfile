# Use an official Python runtime as a parent image
FROM python:3.7
LABEL maintainer="kahihikolo_kaimi@bah.com"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
# ENV DJANGO_ENV dev

# ARG USERNAME=root

# RUN mkdir -p /home/$USERNAME/.vscode-server/extensions \
#     /home/$USERNAME/.vscode-server-insiders/extensions \
#     && chown -R $USERNAME \
#     /home/$USERNAME/.vscode-server \
#     /home/$USERNAME/.vscode-server-insiders

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn
# RUN apt-get update -y && apt-get upgrade -y
# RUN apt-get install vim -y

# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
# RUN useradd appuser && chown -R appuser /code
# USER appuser

# CMD exec gunicorn TimeTracker.wsgi:application --bind 0.0.0.0:8000 --workers 3
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "TimeTracker.wsgi"]