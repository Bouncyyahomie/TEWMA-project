"""Urls for Django appointment app."""
from django.urls import path

from . import views

app_name = 'appointment'
urlpatterns = [
    path('', views.IndexView.as_view(), name="home_page"),
    path("meeting/<int:year>/<int:month>/<int:day>", views.meeting_list, name="meet_list"),
    path("<int:meeting_id>/detail", views.detail, name="detail"),
    path('result/', views.search, name="search"),
    path('<int:meeting_id>/join', views.join, name='join'),
    path('<int:meeting_id>/leave', views.leave, name='leave'),
    path('<int:meeting_id>/participants', views.appointment_participants, name='participants'),
    path('', views.autocomplete, name="autocomplete"),
]
