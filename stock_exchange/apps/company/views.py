from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView,
)
from rest_framework_guardian.filters import ObjectPermissionsFilter
from rest_framework_jwt.serializers import (
    jwt_payload_handler,
    jwt_encode_handler
)

from stock_exchange.apps.company.models import Company
from stock_exchange.apps.company.serializer import (
    CompanyRetrieveSerializer,
    CreateUpdateCompanySerializer,
    ListCompanySerializer
)
from stock_exchange.permissions import CustomObjectPermissions

User = get_user_model()


class CompanyCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Company.objects.all()
    serializer_class = CreateUpdateCompanySerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save(**kwargs)
        payload = jwt_payload_handler(company.user)
        response = {
            'token': jwt_encode_handler(payload)
        }
        return Response(response, status=status.HTTP_201_CREATED)


class UpdateCompanyView(UpdateAPIView):
    """
    Endpoint for updating Company
    """
    permission_classes = [CustomObjectPermissions]
    serializer_class = CreateUpdateCompanySerializer
    queryset = Company.objects.filter(deleted=False)

    def update(self, request, *args, **kwargs):
        company = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        company_instance = serializer.update(company, serializer.validated_data)

        read_serializer = CreateUpdateCompanySerializer(company_instance)
        return Response(read_serializer.data, status=status.HTTP_200_OK)


class RetrieveCompanyDetailsById(RetrieveAPIView):
    """
    Retrieve Company by Id.
    """
    queryset = Company.objects.filter(deleted=False)
    serializer_class = CompanyRetrieveSerializer
    permission_classes = [AllowAny]


class ListCompanyView(ListAPIView):
    """
    Lists companies
    """
    serializer_class = ListCompanySerializer
    queryset = Company.objects.all()
    permission_classes = [AllowAny]


class DeleteCompanyView(DestroyAPIView):
    queryset = Company.objects.all()
    permission_classes = [CustomObjectPermissions]

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
