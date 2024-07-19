from api.models import User
from api.cities import Cities
from api.tasks import request_city_data_task

def register_user(user_id):
  # create user
  user = User.objects.create(id=user_id)
  
  # for city in Cities add a task to queue
  cities = Cities()
  for city_id in cities.get_cities_list():
    request_city_data_task.delay(user.id, city_id)
  return user
  