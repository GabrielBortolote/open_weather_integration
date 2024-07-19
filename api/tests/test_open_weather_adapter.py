import os
from django.test import TestCase
from unittest.mock import patch, Mock
from api.open_weather_adapter import request_city

class TestRequestCity(TestCase):

    @patch('requests.get')
    def test_request_city(self, mock_get):
        # Set up the mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'Test City',
            'main': {
                'temp': 20.0,
                'humidity': 50
            }
        }
        mock_get.return_value = mock_response

        # Call the function under test
        city_data = request_city(city_id='12345')

        # Assertions to ensure the function behaves as expected
        self.assertEqual(city_data, {
            'name': 'Test City',
            'temperature': 20.0,
            'humidity': 50,
        })
        mock_get.assert_called_once_with(
            os.environ.get("OPEN_WEATHER_API_URL") +
            os.environ.get("OPEN_WEATHER_API_ENDPOINT") +
            f'?id=12345&appid={os.environ.get("OPEN_WEATHER_API_KEY")}'
        )
