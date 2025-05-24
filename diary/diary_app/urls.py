from django.urls import path
from .import views

app_name = 'diary_app'

urlpatterns = [
    path('', views.portfolio, name= 'portfolio'),
    path('login/', views.login, name= 'login'),
    path('regist/', views.regist, name= 'regist'),
    path('activate_user/<uuid:token>', views.activate_user, name= 'activate_user'),
    path('home/', views.home, name= 'home'),
]
