from rest_framework import serializers
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin

from stock_exchange.apps.stock.models import Stock
from stock_exchange.apps.utils import default_perm_map


class CreateUpdateStockSerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    def get_permissions_map(self, created):
        current_user = self.context['request'].user
        return default_perm_map(self.Meta.model.__name__, current_user)

    class Meta:
        model = Stock
        fields = (
            'open_amount_in_ngn',
            'high_amount_in_usd',
            'low_amount_in_usd',
            'close_amount_in_usd',
            'volume_amount_in_usd',
            'data_time'
        )

    def create(self, validated_data, **kwargs):
        stock = Stock.objects.create(**validated_data)
        return stock

    def update(self, instance, validated_data, **kwargs):
        instance.open_amount_in_ngn = validated_data.get('open_amount_in_ngn', instance.open_amount_in_ngn)
        instance.high_amount_in_usd = validated_data.get('high_amount_in_usd', instance.high_amount_in_usd)
        instance.low_amount_in_usd = validated_data.get('low_amount_in_usd', instance.low_amount_in_usd)
        instance.close_amount_in_usd = validated_data.get('close_amount_in_usd', instance.close_amount_in_usd)
        instance.volume_amount_in_usd = validated_data.get('volume_amount_in_usd', instance.volume_amount_in_usd)
        instance.data_time = validated_data.get('data_time', instance.data_time)
        instance.save()
        return instance


class ListStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'open_amount_in_ngn',
            'high_amount_in_usd',
            'low_amount_in_usd',
            'close_amount_in_usd',
            'volume_amount_in_usd',
            'data_time',
        )
