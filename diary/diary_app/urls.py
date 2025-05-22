from django.urls import path
from .import views

app_name = 'diary_app'

urlpatterns = [
    path('', views.portfolio, name= 'portfolio'),
    path('login/', views.login, name= 'login'),
    path('regist/', views.regist, name= 'regist'),
]
