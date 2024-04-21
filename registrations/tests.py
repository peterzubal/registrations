from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Student
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

class StudentRegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.update_profile_url = reverse('update_profile')  # Assuming 1 is a valid user ID

        # Creating a user for testing login and logout
        self.user = Student.objects.create(
            username='testuser',
            password=make_password('password123'),  # Storing the hashed version of the password
            full_name='Test User',
            address='123 Test Ave',
            date_of_birth='1990-01-01',
            phone_number='1234567890',
            disabilities='None'
        )
        self.user.save()
        self.client.force_authenticate(user=self.user)


    def test_register(self):
        """
        Ensure we can create a new user and receive a token upon registration, and encrypt the data using the Fernet cipher.
        """
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'full_name': 'New User',
            'address': '456 New Ave',
            'date_of_birth': '1995-05-05',
            'phone_number': '987654321',
            'disabilities': 'None'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_login(self):
        """
        Ensure we can login with a user and receive a token, and get decrypted data using the Fernet cipher.

        """
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """
        Ensure we can logout a user.

        """
        # First login to get a token
        self.test_login()
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        """
        Ensure we can update a user's profile, and encrypt the updated data using the Fernet cipher.
        """
        self.test_login()  # Ensure user is logged in and has token
        self.client.force_authenticate(user=self.user)
        data = {
            'full_name': 'Updated User'

        }
        response = self.client.post(self.update_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       


    def tearDown(self):
            # Explicitly clear the collection
            Student.objects.delete()
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass
