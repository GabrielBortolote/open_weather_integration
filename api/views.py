from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from api.models import User
from api.user_controller import register_user


class UniqueView(View):
    def get(self, request, *args, **kwargs):
      user_id = request.GET.get('user_id', '')
      user = get_object_or_404(User, pk=int(user_id))
      return HttpResponse(user.percentage_status)
    
    def post(self, request, *args, **kwargs):
      user_id = request.POST.get('user_id', '')
      
      # check if the provided ID already exists
      if User.objects.filter(id=user_id).exists():
        return HttpResponse('User ID already exists.', status=409)
      
      # register user and put its requests in the queue
      register_user(user_id)

      return HttpResponse("This is a post")