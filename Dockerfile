FROM python:3.10-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# set work directory
WORKDIR /code

# install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /code/

# view dir files
RUN ls -al

RUN ["chmod", "755", "entrypoint.sh"]
ENTRYPOINT ["/code/entrypoint.sh"]