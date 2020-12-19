#################
# Stock exchange development Image
#################
FROM base

ENV DJANGO_SETTINGS_MODULE stock_exchange.settings

COPY       stock_exchange /var/app/stock_exchange
COPY       pytest.ini /var/app/pytest.ini
COPY       manage.py /var/app/manage.py
COPY       quick_test_seeding.py /var/app/quick_test_seeding.py
COPY       scripts/run_local.sh /var/app/run_local.sh

RUN        chmod +x run_local.sh
EXPOSE     8001
CMD        ["/var/app/run_local.sh"]