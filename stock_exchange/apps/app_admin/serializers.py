from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.fields import EmailField, CharField
from rest_framework.validators import UniqueValidator

from stock_exchange.apps.app_admin.models import AppAdmin

User = get_user_model()


class CreateAdminSerializer(serializers.ModelSerializer):
    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=False)
    password = CharField(required=False)

    class Meta:
        model = AppAdmin
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        logged_in_user = self.context['request'].user
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_app_admin_user(
            email=email,
            password=password,
        )
        admin = AppAdmin.objects.create(
            user=user,
            created_by=logged_in_user,
            **validated_data
        )
        return admin


class RetrieveAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppAdmin
        fields = ('first_name', 'last_name',)
