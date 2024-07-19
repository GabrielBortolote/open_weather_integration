from django.test import TestCase
from unittest.mock import patch
from api.models import User
from api.views import register_user

class ApiViewsTestCase(TestCase):
    
    @patch('api.cities.Cities.get_cities_list')
    @patch('api.tasks.request_city_data_task.delay')
    def test_register_user(self, mock_delay, mock_get_cities_list):
        # Mock Cities.get_cities_list to return a list of city IDs
        mock_get_cities_list.return_value = [1, 2, 3]

        # Call the register_user function
        user_id = 'unique_user_id'
        user = register_user(user_id)

        # Assertions to ensure the function behaves as expected
        self.assertEqual(user, User.objects.get(id=user_id))
        
        # Verify that request_city_data_task.delay was called for each city
        mock_delay.assert_any_call(user.id, 1)
        mock_delay.assert_any_call(user.id, 2)
        mock_delay.assert_any_call(user.id, 3)
        self.assertEqual(mock_delay.call_count, 3)