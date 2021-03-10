from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    # test the users API public
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        # test creating user with valid payload is successful
        payload = {
            'email': 'test@gmail.com',
            'password': 'test123',
            'name': 'Test Python'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_already_exists(self):
        # user already exists
        payload = {
            'email': 'test1@gmail.com',
            'password': 'test098'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        # password mush be more than 5 characters
        payload = {
            'email': 'test2@gmail.com',
            'password': 'te',
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
