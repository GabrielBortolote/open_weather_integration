from django.urls import path
from api.views import UniqueView

urlpatterns = [
    path("", UniqueView.as_view(), name="index"),
]