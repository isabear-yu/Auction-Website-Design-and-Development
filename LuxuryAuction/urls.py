from django.urls import path
from LuxuryAuction import views
from django.conf.urls import include, url


urlpatterns = [
    path('', views.calculate_distance_view, name='calculate-view'),
    path('paid', views.paid, name='paid'),
    
]
