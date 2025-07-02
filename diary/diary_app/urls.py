from django.urls import path
from .import views
from. views import DiaryInspectionListView

app_name = 'diary_app'

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('regist/', views.regist, name='regist'),
    # path('activate_user/<uuid:token>', views.activate_user, name='activate_user'),
    # path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('reflection/', views.reflection, name='reflection'),
    path('my_page/', views.my_page, name='my_page'),
    path('change_password/', views.change_password, name='change_password'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
    path('today_input/<int:year>/<int:month>/<int:day>/', views.today_input, name='today_input'),
    path('diary_inspection/<int:year>/<int:month>/<int:day>/', DiaryInspectionListView.as_view(), name='diary_inspection'),
    
]
