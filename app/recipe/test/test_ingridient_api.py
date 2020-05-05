from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingridient

from recipe.serializers import IngridientSerializer


INGRIDIENTS_URL = reverse('recipe:ingridient-list')


class PublicIngridientApiTests(TestCase):
    """Test publicly available ingridients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login is requiered to access the end point"""
        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngridientsApiTests(TestCase):
    """Test the private ingridient API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@rogelio',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingridient_list(self):
        """Test retrieving a list of ingridients"""
        Ingridient.objects.create(user=self.user, name='Kale')
        Ingridient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGRIDIENTS_URL)

        ingridient = Ingridient.objects.all().order_by('-name')
        serializer = IngridientSerializer(ingridient, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingridients_limited_to_user(self):
        """Test only ingridients for auth user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@rogelio.com',
            'otherpass'
        )
        Ingridient.objects.create(user=user2, name='Vinegar')
        ingridient = Ingridient.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingridient.name)
