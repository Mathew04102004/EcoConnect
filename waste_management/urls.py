from django.urls import path
from . import views
from waste_management.views import login_view
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import user_login, admin_login, staff_login
from .views import user_dashboard,admin_dashboard,staff_dashboard
app_name = "waste_management"

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.home, name='home'),
    path("login/", login_view, name="login_view"),
    path('register/', views.register, name='register'),
    path('schedule/', views.schedule, name='schedule'),
    path('track/', views.track, name='track'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create_account/', views.create_account_view, name='create_account'),
    path('pickup_schedule/', views.pickup_schedule, name='pickup_schedule'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cancel_pickup/<int:pickup_id>/', views.cancel_pickup, name='cancel_pickup'),
    path('admin_portal/', views.admin_portal, name='admin_portal'),
    path('staff-portal/', views.staff_portal_view, name="staff_portal"),    
    path('logout/', views.logout_view, name='logout'),
    path("user_login/", user_login, name="user_login"),
    path("admin_login/", admin_login, name="admin_login"),
    path("staff_login/", staff_login, name="staff_login"),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/staff/', staff_dashboard, name='staff_dashboard'),
]
