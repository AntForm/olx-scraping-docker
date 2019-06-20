FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir /requirements
ADD requirements.txt /requirements
RUN pip3 install -r /requirements/requirements.txt
WORKDIR /code
