ARG BASE_IMAGE=python:3.12-slim-bookworm
###########
# BUILDER #
###########

# pull official base image
FROM $BASE_IMAGE as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

# install python dependencies
COPY ./requirements-prod.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements-prod.txt


#########
# FINAL #
#########

# pull official base image
FROM $BASE_IMAGE

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd
COPY --from=builder /wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.prod.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]