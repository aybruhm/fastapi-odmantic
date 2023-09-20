# pull from tiangolo image
FROM tiangolo/uvicorn-gunicorn:python3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements to working directory
COPY ./requirements.txt /requirements.txt

# install dependencies
RUN pip install -U pip
RUN --mount=type=cache,target=/root/.cache \
    pip install -r /requirements.txt

# set working directory
WORKDIR /template_be

# Set python path to working directory in docker
ENV PYTHONPATH=/template_be/backend/

# Copy current directory to working directory in docker
COPY ./ /template_be/
