from django.urls import path
from django.contrib.auth import views as auth_views  # Import the built-in login view
from . import views

urlpatterns = [
    path('', views.register, name='register'),  # Set the register view as the index (home) page
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='hotel/login.html'), name='login'),  # Add the login view
    path('make_reservation/', views.make_reservation, name='make_reservation'),  # Add the reservation view
]