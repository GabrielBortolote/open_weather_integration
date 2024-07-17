import time
from celery import shared_task

@shared_task
def request_city_data_task(user_id, city_id):
    print(f'Requesting city {city_id} for user {user_id}')
    time.sleep(10)
    return user_id
