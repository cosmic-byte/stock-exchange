FROM python:3.6-slim

ENV APP_DIR /var/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE stock_exchange.ci_settings

RUN mkdir    /var/app
WORKDIR    /var/app

COPY requirements.txt /var/app/requirements.txt
COPY test-requirements.txt /var/app/test-requirements.txt

RUN pip install -r /var/app/requirements.txt -r /var/app/test-requirements.txt

COPY       stock_exchange /var/app/stock_exchange
COPY       pytest.ini /var/app/pytest.ini
COPY       manage.py /var/app/manage.py
COPY       scripts/run_test.sh /var/app/run_test.sh

RUN        chmod +x run_test.sh
CMD        ["sh run_test.sh"]