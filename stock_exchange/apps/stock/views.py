from django.db import transaction, models
from django.db.models import Func, Max
from django_elasticsearch_dsl_drf.filter_backends import CompoundSearchFilterBackend
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    ListAPIView, GenericAPIView,
)


from stock_exchange.apps.company.models import Company
from stock_exchange.apps.stock.document_serializers import StockDocumentSerializer
from stock_exchange.apps.stock.documents import StockDocument
from stock_exchange.apps.stock.models import Stock
from stock_exchange.apps.stock.serializer import CreateUpdateStockSerializer, ListStockSerializer
from stock_exchange.permissions import CustomObjectPermissions
from stock_exchange.util import get_object_or_400, get_object_or_none


class CreateStockDataView(CreateAPIView):
    permission_classes = (DjangoModelPermissions,)
    queryset = Stock.objects.all()
    serializer_class = CreateUpdateStockSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        company_id = kwargs.get('company_id')
        company = get_object_or_400(
            Company,
            id=company_id,
            deleted=False,
            error_message='Company with id {} does not exist'.format(company_id),
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock_instance = serializer.save(company=company)

        read_serializer = CreateUpdateStockSerializer(stock_instance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class UpdateStockDataView(UpdateAPIView):
    """
    Endpoint for updating Stock Data
    """
    permission_classes = [CustomObjectPermissions]
    serializer_class = CreateUpdateStockSerializer
    queryset = Stock.objects.filter(deleted=False)

    def update(self, request, *args, **kwargs):
        stock = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_stock = serializer.update(stock, serializer.validated_data)

        read_serializer = CreateUpdateStockSerializer(updated_stock)
        return Response(read_serializer.data, status=status.HTTP_200_OK)


class ListStockView(ListAPIView):
    """
    Lists all stock
    """
    serializer_class = ListStockSerializer
    queryset = Stock.objects.all()
    permission_classes = [AllowAny]


class SearchStockView(BaseDocumentViewSet):
    """The StockDocument view."""

    document = StockDocument
    serializer_class = StockDocumentSerializer
    pagination_class = PageNumberPagination
    filter_backends = [CompoundSearchFilterBackend]
    search_fields = (
        'company_name',
        'company_symbol',
    )


class GetTimeSeriesCompanyStockData(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = Stock.objects.filter()
    serializer_class = ListStockSerializer

    def get(self, request, *args, **kwargs):
        """
        Get a time interval stock data for a company.
        - Symbol: this is a symbol denoting the company eg symbol=IBM
        - interval: this is a time series interval for stock data.
                    It must be one of the following:
                    - DAILY
                    - WEEKLY
                    - MONTHLY
        """
        time_series = ('daily', 'weekly', 'monthly')
        company_symbol = kwargs.get('symbol')
        time_interval = kwargs.get('interval')

        company = get_object_or_none(Company, company_symbol=company_symbol)
        if all([company, time_interval]) and time_interval.lower() in time_series:
            # company_stock = Stock.objects.filter(deleted=False, company=company)
            # if time_interval.lower() == 'daily':
            #     company_stock = company_stock.datetimes('data_time', 'day')
            # elif time_interval.lower() == 'weekly':
            #     company_stock = company_stock.datetimes('data_time', 'week')
            # elif time_interval.lower() == 'monthly':
            #     # company_stock = (company_stock
            #     #          .annotate(month_added=Month('data_time'))
            #     #          .values('data_time__date', 'id')
            #     #          .order_by('month_added'))
            #     company_stock = company_stock.datetimes('data_time', 'month')
            # company_stock = company_stock.annotate(open=Max("open_amount_in_ngn")).values('id', 'data_time', 'open')

            company_stock = Stock.objects.raw('SELECT CONCAT(EXTRACT(YEAR FROM data_time), EXTRACT(MONTH FROM data_time)) as data_time, '
                                              'id, open_amount_in_ngn '
                                              'FROM stock_stock GROUP BY data_time, id')
            stocks = ListStockSerializer(company_stock, many=True)

            return Response(stocks.data, status=status.HTTP_200_OK)
            # return Response(self.get_response(company, time_interval, company_stock), status=status.HTTP_200_OK)
        return Response('Invalid stock filter', status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_response(company, time_interval, stock_data):
        data = {
            "meta": {
                "information": f"{time_interval} Prices (open, high, low, close) and Volumes",
                "symbol": company.company_symbol,
            },
            "time_series": {

            }
        }

        temp_data = {}
        for _data in stock_data:
            temp_data['kk'] = _data
        data['time_series'] = temp_data
        return data


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()
