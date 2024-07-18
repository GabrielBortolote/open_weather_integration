import time
import logging
from celery import shared_task
from api.open_weather_adapter import request_city
from api.models import User, UserCityRequest

@shared_task
def request_city_data_task(user_id, city_id):
    start_time = time.time()

    logging.info(f"Requesting city {city_id} for user {user_id}")

    # request
    city_data = request_city(city_id)

    # save
    user_city_request = UserCityRequest.objects.create(
        user=User.objects.get(pk=user_id),
        city_id=city_id,
        city_name=city_data['name'],
        temperature=city_data['temperature'],
        humidity=city_data['humidity'],
    )

    # grant that this task takes at least 1 second to execute
    end_time = time.time()
    duration = end_time - start_time
    if duration < 1:
      time.sleep(1-duration)
    
    return user_city_request.pk
