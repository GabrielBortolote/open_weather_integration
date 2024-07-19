from django.test import TestCase, Client
from django.urls import reverse
from api.models import User, UserCityRequest
from unittest.mock import patch

class UniqueViewTests(TestCase):
    
  def setUp(self):
    self.client = Client()
    self.url = reverse('index')

  @patch('api.cities.Cities.get_cities_list')
  def test_get_request(self, mock_get_cities_list):
    # define mock

    #       0   20 40 60       100
    cities = [1, 2, 3, 4, 5]
    mock_get_cities_list.return_value = cities

    # prepare scenario
    user = User.objects.create(
        id='unique_id'
    )

    response = self.client.get(self.url, {'user_id': 'unique_id'})
    self.assertEqual(response.status_code, 200)
    decoded_response = response.content.decode('utf-8')
    self.assertEqual(decoded_response, '0.0')

    for i, city in enumerate(cities):
      UserCityRequest.objects.create(
        user=user,
        city_id=city,
        city_name=f'city {city}',
        temperature=20.0,
        humidity=50,
      )
      response = self.client.get(self.url, {'user_id': 'unique_id'})
      self.assertEqual(response.status_code, 200)
      percentage_completed = ((i+1) * 100) / len(cities)
      decoded_response = response.content.decode('utf-8')
      self.assertEqual(decoded_response, f'{percentage_completed}')


  def test_get_request_missing_user(self):
    response = self.client.get(self.url, {'user_id': 'unique_id'})
    self.assertEqual(response.status_code, 404)


  @patch('api.cities.Cities.get_cities_list')
  @patch('api.tasks.request_city_data_task.delay')
  def test_post_request(self, mock_delay, mock_get_cities_list):
    # define mock
    mock_get_cities_list.return_value = [1, 2, 3]

    # creating user
    response = self.client.post(self.url, {'user_id': 'unique_id'})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(User.objects.count(), 1)
    self.assertEqual(User.objects.first().id, 'unique_id')
    self.assertEqual(mock_delay.call_count, 3)

    # create another user with same ID
    response = self.client.post(self.url, {'user_id': 'unique_id'})
    self.assertEqual(response.status_code, 409)
    self.assertEqual(User.objects.count(), 1)
    self.assertEqual(mock_delay.call_count, 3)

