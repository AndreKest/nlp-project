FROM python:3.8-slim-buster

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Requirements
ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt
RUN python -m spacy download de_core_news_lg

ADD . /usr/src/app

ENV FLASK_APP /usr/src/app/src/app.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]