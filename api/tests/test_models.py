from unittest.mock import patch
from django.test import TestCase
from api.models import User, UserCityRequest

class UserModelTests(TestCase):
  def setUp(self):
    self.user = User.objects.create(id='unique_id')

  @patch('api.models.Cities')
  def test_percentage_status(self, mock_cities):
    # Configure the mock to return a total of 100 cities
    mock_cities.return_value.total_number_of_cities.return_value = 100

    # Create some UserCityRequest instances
    for i in range(10):
      UserCityRequest.objects.create(
        user=self.user,
        city_id=i,
        city_name=f'City {i}',
        temperature=20,
        humidity=50
      )
    # Assert that the percentage_status method returns the correct value
    self.assertEqual(self.user.id, 'unique_id')
    self.assertEqual(self.user.number_of_cities_requested(), 10)
    self.assertEqual(self.user.percentage_status(), 10)

  def test_number_of_cities_requested(self):
    # Create some UserCityRequest instances
    for i in range(10):
      UserCityRequest.objects.create(
        user=self.user,
        city_id=i,
        city_name=f'City {i}',
        temperature=20,
        humidity=50
      )
    # Assert that the number_of_cities_requested method returns the correct value
    self.assertEqual(self.user.number_of_cities_requested(), 10)

class UserCityRequestModelTests(TestCase):
  def setUp(self):
    self.user = User.objects.create(id='unique_id')
    self.user_city_request = UserCityRequest.objects.create(
      user=self.user,
      city_id=1,
      city_name='Test City',
      temperature=20,
      humidity=50
    )

  def test_user_city_request_creation(self):
    # Assert that the UserCityRequest instance was created correctly
    self.assertEqual(self.user_city_request.user, self.user)
    self.assertEqual(self.user_city_request.city_id, 1)
    self.assertEqual(self.user_city_request.city_name, 'Test City')
    self.assertEqual(self.user_city_request.temperature, 20)
    self.assertEqual(self.user_city_request.humidity, 50)