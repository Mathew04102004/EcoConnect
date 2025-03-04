from django.contrib import admin
from django.urls import path
from waste_management import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),  
    path('about/', views.about, name='about'),  
    path('services/', views.services, name='services'),  
    path('contact/', views.contact, name='contact'),  
    path('login/', views.login_view, name='login'),
    path('create-account/', views.create_account_view, name='create_account'),
    path('pickup_schedule/', views.pickup_schedule, name='pickup_schedule'),

]
