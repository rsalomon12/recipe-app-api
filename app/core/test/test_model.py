from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@rogelio.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """"Test creeating a new user with an email is succesful"""
        email = 'rogelio@test.com'
        password = 'testpass!!'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'rogelio@TEST.com'
        user = get_user_model().objects.create_user(email, 'erjeje')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'rogelio2@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingridient_str(self):
        """Test ingridient string representation"""
        ingridient = models.Ingridient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingridient), ingridient.name)
