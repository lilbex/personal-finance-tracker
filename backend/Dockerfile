# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY ./backend/requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the Django project into the container
COPY ./backend /code/
