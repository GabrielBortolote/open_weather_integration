import csv
import os
from django.conf import settings

class Cities:
  def __init__(self):
    self.file_path = self.get_cities_file_path()

  def get_cities_file_path(self) -> str:
   return os.path.join(
     settings.BASE_DIR,
     'cities.csv'
  )
  
  def get_cities_list(self) -> list:
    rows = []
    with open(self.file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header
        for row in reader:
            if row:  # Check if the row is not empty
                rows.append(row[0])  # Append the single column value
    return rows
  
  def total_number_of_cities(self):
    return len(self.get_cities_list())