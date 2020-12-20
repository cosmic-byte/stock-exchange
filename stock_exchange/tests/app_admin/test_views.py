import pytest
from django.urls import reverse
from rest_framework import status

from stock_exchange.tests.test_utils import authenticate_user


class TestAppAdminView:

    @pytest.mark.django_db
    def test_create_app_admin_by_anonymous_should_fail(self, api_client):
        payload = {
            'email': 'ownerx@example.com',
            'password': 'password',
            'first_name': 'owner',
            'last_name': 'owner',
        }
        url = reverse('app_admin:app_admin-create')
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_create_app_admin_by_admin_success(self, app_admin, api_client):
        client = authenticate_user(api_client, app_admin.user, admin_user=True)
        payload = {
            'email': 'ownerx@example.com',
            'password': 'password',
            'first_name': 'owner',
            'last_name': 'owner',
        }
        url = reverse('app_admin:app_admin-create')
        response = client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
