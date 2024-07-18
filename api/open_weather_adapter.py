import requests
import os

def request_city(city_id):
  # make url
  key = os.environ.get("OPEN_WEATHER_API_KEY")
  url = os.environ.get("OPEN_WEATHER_API_URL")
  endpoint = os.environ.get("OPEN_WEATHER_API_ENDPOINT")
  query_parameters = f'?id={city_id}&appid={key}'
  complete_url = url+endpoint+query_parameters
  
  # perform request
  response = requests.get(complete_url)

  # extract and return data
  city_name = response.json()['name']
  temperature = response.json()['main']['temp']
  humidity = response.json()['main']['humidity']
  return {
    'name': city_name,
    'temperature': temperature,
    'humidity': humidity,
  }