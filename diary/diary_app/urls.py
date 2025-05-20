from django.urls import path
from .import views

app_name = 'diary_app'

urlpatterns = [
    path('', views.portforlio, name= 'portforlio'),
]
