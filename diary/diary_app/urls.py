from django.urls import path
from .import views

app_name = 'diary_app'

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('regist/', views.regist, name='regist'),
    path('activate_user/<uuid:token>', views.activate_user, name='activate_user'),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
