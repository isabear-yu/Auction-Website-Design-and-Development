from django.urls import path
from welcome import views


urlpatterns = [
    path('register', views.register_action, name='register'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('verify/', views.email_verify, name='verify'),
]

