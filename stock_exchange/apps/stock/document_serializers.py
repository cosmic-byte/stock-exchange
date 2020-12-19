from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from stock_exchange.apps.stock.documents import StockDocument


class StockDocumentSerializer(DocumentSerializer):
    """Serializer for the Stock document."""

    class Meta(object):
        """Meta options."""
        document = StockDocument
        fields = [
            'id',
            'company_name',
            'company_symbol',
        ]
