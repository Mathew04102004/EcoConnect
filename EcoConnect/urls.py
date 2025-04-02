from django.contrib import admin
from django.urls import path
from waste_management import views
from .views import user_login, admin_login, staff_login,login_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),  
    path('about/', views.about, name='about'),  
    path('services/', views.services, name='services'),  
    path('contact/', views.contact, name='contact'),  
    path('login/', login_view, name='login_view'),
    path('login/', login_view, name='login'),
    path('create-account/', views.create_account_view, name='create_account'),
    path('pickup_schedule/', views.pickup_schedule, name='pickup_schedule'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('schedules/', views.schedules, name='schedules'),
    path('cancel_pickup/<int:pickup_id>/', views.cancel_pickup, name='cancel_pickup'),
    path('admin_portal/', views.admin_portal, name='admin_portal'),
    path("staff-portal/", views.staff_portal_view, name="staff_portal"),
    path('logout/', views.logout_view, name='logout'),
    path("user_login/", user_login, name="user_login"),
    path("admin_login/", admin_login, name="admin_login"),
    path("staff_login/", staff_login, name="staff_login"),
]
