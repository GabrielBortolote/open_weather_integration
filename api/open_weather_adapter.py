import requests

def request_city(city_id):
  API_key = 'dc3ec2071d2a5bac54f3fd68634a54d5'
  url = f'https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_key}'
  response = requests.get(url)

  city_name = response.json()['name']
  temperature = response.json()['main']['temp']
  humidity = response.json()['main']['humidity']

  return {
    'name': city_name,
    'temperature': temperature,
    'humidity': humidity,
  }