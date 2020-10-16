"""Urls for Django appointment app."""
from django.urls import path

from . import views


app_name='appointment'
urlpatterns = [
    path('', views.IndexView.as_view(), name="home_page"),
]
