import logging

from api.models import User
from api.cities import Cities
from api.tasks import request_city_data_task

def register_user(user_id):
  user = User.objects.create(id=user_id)
  put_user_requests_on_queue(user)
  return user

def put_user_requests_on_queue(user:User):
  cities = Cities()
  for city_id in cities.get_cities_list():
    try:
      request_city_data_task.delay(user.id, city_id)
    except:
      logging.exception('an error occurred')
