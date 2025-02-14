from django.contrib import admin
from django.urls import path
from waste_management import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),  # Fix: Changed 'home' to 'index' (which exists in views.py)
    path('about/', views.about, name='about'),  
    path('services/', views.services, name='services'),  
    path('contact/', views.contact, name='contact'),  
    path('login/', views.user_login, name='login'),  # Using `user_login` instead of `login_view`
    path('create-account/', views.create_account_view, name='create_account'),
]
