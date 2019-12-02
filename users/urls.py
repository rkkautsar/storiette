from .views import UserView
from django.urls import path

urlpatterns = [
    path('get/', UserView.as_view()),
]
