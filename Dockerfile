FROM python:3.10-alpine

WORKDIR /app

RUN pip install pipenv

ADD ./Pipfile /app/
ADD ./Pipfile.lock /app/

RUN pipenv sync

ADD . /app/

CMD ["python", "src/placebot.py"]
