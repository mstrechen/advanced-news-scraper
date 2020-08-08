FROM python:3.7.8-buster
EXPOSE 80
WORKDIR /app

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY . .
RUN chmod +x run.sh

ENTRYPOINT ["/app/run.sh"]