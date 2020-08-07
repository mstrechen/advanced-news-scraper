FROM python:3.7.8-buster
EXPOSE 80
WORKDIR /app

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv sync

COPY ./admin ./admin
COPY run.py ./

ENTRYPOINT pipenv run python run.py