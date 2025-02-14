from django.urls import path
from . import views
from waste_management.views import login_view

urlpatterns = [
     path('', views.index, name='index'),
    # path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('schedule/', views.schedule, name='schedule'),
    path('track/', views.track, name='track'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create_account/', views.create_account_view, name='create_account'),
]
