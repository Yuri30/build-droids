# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /droid_service

WORKDIR /droid_service

# Copy requirements to the container
COPY Pipfile Pipfile.lock /droid_service/

# Install the requirements to the container
RUN pip install pipenv && pipenv install --system

ADD . /droid_service/


