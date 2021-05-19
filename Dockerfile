FROM python:3.7.4-slim-stretch

RUN apt-get update && apt-get install -y --no-install-recommends libmagic1

RUN pip install virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN mkdir -p $VIRTUAL_ENV && virtualenv $VIRTUAL_ENV
# Make sure we use the virtualenv:
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements/requirements.txt .
COPY requirements/deploy-requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt -r deploy-requirements.txt

RUN adduser --disabled-password --gecos "" pyuser

COPY . /s3browser
RUN chown -R pyuser:pyuser /s3browser
USER pyuser