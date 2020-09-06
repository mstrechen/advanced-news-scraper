FROM python:3.7.8-buster
EXPOSE 80

WORKDIR /app

RUN apt-get update
RUN apt-get install -y chromium-driver

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY . .
RUN chmod +x run.sh

ENTRYPOINT ["/app/run.sh"]