from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.fields import EmailField, CharField
from rest_framework.validators import UniqueValidator
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin

from stock_exchange.apps.company.models import Company
from stock_exchange.apps.utils import default_perm_map
from stock_exchange.util import get_object_or_none

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class CreateUpdateCompanySerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=False)
    password = CharField(required=False)

    def get_permissions_map(self, created):
        current_user = get_object_or_none(User, email=self.validated_data.get('email'))
        return default_perm_map(self.Meta.model.__name__, current_user)

    class Meta:
        model = Company
        fields = (
            'email',
            'password',
            'ref_first_name',
            'ref_last_name',
            'ref_phone_number',
            'company_name',
            'company_symbol',
            'website',
            'address',
        )

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_company_user(
            email=email,
            password=password,
        )

        company = Company.objects.create(
            user=user,
            **validated_data
        )
        return company

    def update(self, instance, validated_data, **kwargs):
        instance.ref_first_name = validated_data.get('ref_first_name', instance.ref_first_name)
        instance.ref_last_name = validated_data.get('ref_last_name', instance.ref_last_name)
        instance.ref_phone_number = validated_data.get('ref_phone_number', instance.ref_phone_number)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.company_symbol = validated_data.get('company_symbol', instance.company_symbol)
        instance.address = validated_data.get('address', instance.address)
        instance.website = validated_data.get('website', instance.website)
        instance.save()
        return instance


class UserRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('email', 'uid', 'groups', 'is_active')
        read_only_fields = ('groups',)


class CompanyRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    user = UserRetrieveSerializer()

    class Meta:
        model = Company
        fields = (
            'user',
            'id',
            'ref_first_name',
            'ref_last_name',
            'ref_phone_number',
            'company_name',
            'company_symbol',
            'website',
            'address',
        )


class ListCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = (
            'id',
            'company_name',
            'company_symbol',
            'website',
            'address',
        )
