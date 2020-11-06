"""Urls for Django appointment app."""
from django.urls import path

from . import views

app_name = 'appointment'
urlpatterns = [
    path('', views.IndexView.as_view(), name="home_page"),
    path("meeting/<int:year>/<int:month>/<int:day>", views.meeting_list, name="meet_list"),
    path("<int:meeting_id>/detail", views.detail, name="detail"),
    path('result/', views.search, name="search"),
]
