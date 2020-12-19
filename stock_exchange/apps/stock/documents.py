from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer

from stock_exchange.apps.stock.models import Stock

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@registry.register_document
class StockDocument(Document):
    id = fields.TextField(attr='id')
    company_name = fields.TextField(
        attr='company_name_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    company_symbol = fields.TextField(
        attr='company_symbol_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    class Index:
        name = 'stocks'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = Stock
        fields = []
