import os
import csv
import unittest.mock as mock
from django.test import TestCase
from django.conf import settings
from api.cities import Cities

class CitiesTestCase(TestCase):

  def test_default_file_path(self):
    # Instantiate the Cities class
    cities = Cities()

    default_csv_file_path = os.path.join(
      settings.BASE_DIR,
      'cities.csv'
    )
    self.assertEqual(cities.get_cities_file_path(), default_csv_file_path)

  @mock.patch('api.cities.Cities.get_cities_file_path')
  def test_1_city_file(self, mock_get_cities_file_path):
    # Set the mock return value
    mock_get_cities_file_path.return_value = os.path.join(
      settings.BASE_DIR, 'api', 'tests', 'fixtures', '1_city.csv'
    )

    # Instantiate the Cities class
    cities = Cities()

    self.assertEqual(cities.get_cities_file_path(), mock_get_cities_file_path.return_value)
    self.assertEqual(cities.get_cities_list(), [
      "unique_id_1"
    ])
    self.assertEqual(cities.total_number_of_cities(), 1)

  @mock.patch('api.cities.Cities.get_cities_file_path')
  def test_5_cities_file(self, mock_get_cities_file_path):
    # Set the mock return value to point to the fixture file
    mock_get_cities_file_path.return_value = os.path.join(
      settings.BASE_DIR, 'api', 'tests', 'fixtures', '5_cities.csv'
    )

    # Instantiate the Cities class
    cities = Cities()

    self.assertEqual(cities.get_cities_file_path(), mock_get_cities_file_path.return_value)
    self.assertEqual(cities.get_cities_list(), [
      "unique_id_1",
      "unique_id_2",
      "unique_id_3",
      "unique_id_4",
      "unique_id_5",
    ])
    self.assertEqual(cities.total_number_of_cities(), 5)