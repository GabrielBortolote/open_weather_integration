from django.db import models

from api.cities import Cities

class User(models.Model):

  # fields
  id = models.CharField(max_length=100, unique=True, primary_key=True)
  created_at = models.DateTimeField(auto_now_add=True)
  

  # methods
  def percentage_status(self):
    """Returns with the percentage of the POST progress ID (collected
    cities completed) until the current moment"""
    
    already_requested = self.number_of_cities_requested()
    cities = Cities()
    total_to_request = cities.total_number_of_cities()
    return (already_requested * 100)/total_to_request
    

  def number_of_cities_requested(self):
    return UserCityRequest.objects.filter(
      user=self
    ).count()


class UserCityRequest(models.Model):
  user = models.ForeignKey('api.User', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  city_id = models.IntegerField()
  city_name = models.CharField(max_length=400)
  temperature = models.IntegerField()
  humidity = models.IntegerField()