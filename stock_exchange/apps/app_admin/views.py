from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework_guardian.filters import ObjectPermissionsFilter

from stock_exchange.apps.app_admin.models import AppAdmin
from stock_exchange.apps.app_admin.serializers import CreateAdminSerializer, RetrieveAdminSerializer
from stock_exchange.permissions import CustomObjectPermissions
from stock_exchange.util import get_object_or_400

User = get_user_model()


class AdminViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = AppAdmin.objects.all()
    serializer_class = CreateAdminSerializer
    permission_classes = [CustomObjectPermissions]
    filter_backends = [ObjectPermissionsFilter]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_400(queryset, user=self.request.user)
        return obj

    def retrieve(self, request, *args, **kwargs):
        serializer = RetrieveAdminSerializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
