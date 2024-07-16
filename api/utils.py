import csv
import os
from django.conf import settings
from django.apps import apps


def register_user(user_id):
  """Register user and put its requests into the queue"""
  User = apps.get_model('api', 'User')
  user = User.objects.create(id=user_id)
  return user

def total_number_of_cities(self):
  return count_lines_in_csv(os.path.join(
     settings.BASE_DIR,
     'cities.csv'
  ))

def count_lines_in_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header
        line_count = sum(1 for row in csv_reader)
    return line_count

class OpenWeatherAdapter:
  def __init__(self):
    pass