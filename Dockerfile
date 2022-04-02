FROM python:3-alpine

WORKDIR /app

RUN pip install pipenv

ADD ./Pipfile /app/
ADD ./Pipfile.lock /app/

RUN pipenv install --system --deploy --ignore-pipfile

ADD . /app/

CMD ["python", "src/placebot.py"]
