from users.models import CustomUser
from django.test import TestCase
from rest_framework.test import APIClient

from users.views import UserAPIView, UserLoginAPIView

from .models import Profile
from .serializers import UserRegisterationSerializer, CustomUserSerializer

class UserRegistrationAPITestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

  def test_successful_registration(self):
    data = {
      'email': 'test1@example.com',
      'username': 'testuser1',
      'password': 'strongpassword'
    }
    response = self.client.post('/api/user/register/', data=data, format='json')
    self.assertEqual(response.status_code, 201)


  
class UserLoginAPITestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    user = CustomUser.objects.create_user(email='test1@example.com', username='testuser1', password='strongpassword')
    user.save()

  def test_successful_login(self):
    data = {
      'email': 'test1@example.com',
      'password': 'strongpassword'
    }
    response = self.client.post('/api/user/login/', data=data, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertIn('tokens', response.data)
    # serializer = CustomUserSerializer(instance=UserLoginAPIView)
    # self.assertEqual(response.data, serializer.data)
  def test_invalid_credentials(self):
    data = {
      'email': 'existing@example.com',
      'password': 'wrongpassword'
    }
    response = self.client.post('/api/user/login/', data=data, format='json')
    self.assertEqual(response.status_code, 400)

  def test_user_not_found(self):
    data = {
      'email': 'nonexistent@example.com',
      'password': 'anypassword'
    }
    response = self.client.post('/api/user/login/', data=data, format='json')
    self.assertEqual(response.status_code, 400)
