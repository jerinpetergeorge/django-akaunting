FROM python:3.9 AS base

LABEL maintainer="Jerin Peter George <jerinpetergeorge@gmail.com>"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a new directory to keep the project files
RUN mkdir /django-akaunting

# Copy local contents into container
COPY ./ /django-akaunting/

# Setting newly created directory as PWD
WORKDIR /django-akaunting/

# Creating a non-root user
RUN useradd -m akaunting-user

# Switching the user
USER akaunting-user

# Adding user's bin path to `PATH` variable
ENV PATH "$PATH:/home/akaunting-user/.local/bin"

# Installing pip packages
RUN pip install pip -U

FROM base AS Production
RUN pip install --no-cache-dir -r requirements/production.txt -U

FROM production AS Test
RUN pip install --no-cache-dir -r requirements/production.txt -U
RUN pip install --no-cache-dir -r requirements/test.txt -U

FROM base as Developement
RUN pip install --no-cache-dir -r requirements/dev.txt -U
