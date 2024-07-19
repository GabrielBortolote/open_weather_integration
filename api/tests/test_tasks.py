from api.tasks import request_city_data_task
from api.models import User, UserCityRequest
from django.test import TestCase
from unittest.mock import patch

class TestRequestCityDataTask(TestCase):
    
  def setUp(self) -> None:
    self.user = User.objects.create(
      id='unique_id'
    )

  @patch('api.tasks.request_city')
  def test_request_city_data_task(self, mock_request_city):
    # Mock request_city to return a predefined city data
    mock_city_data = {
      'name': 'Test City',
      'temperature': 20.0,
      'humidity': 50,
    }
    mock_request_city.return_value = mock_city_data
          
    # Call the task
    self.assertEqual(UserCityRequest.objects.count(), 0)
    task_result = request_city_data_task(self.user.id, 123)
      
    # Assertions
    created_log = UserCityRequest.objects.first()
    self.assertEqual(task_result, created_log.pk)
    self.assertEqual(UserCityRequest.objects.count(), 1)
    self.assertEqual(created_log.user.id, self.user.id)
    self.assertEqual(created_log.city_id, 123)
    self.assertEqual(created_log.city_name, 'Test City')
    self.assertEqual(created_log.temperature, 20.0)
    self.assertEqual(created_log.humidity, 50)
