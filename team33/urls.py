"""team33 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from LuxuryAuction import views

urlpatterns = [
    path('', views.home_page_action, name='homePage'),
    path('welcome/', include('welcome.urls')),
    path('profile', views.profile_action, name='profile'),
    path('bidding/<int:id>', views.bidding_action, name='bidding'),
    path('get-CurrentBid', views.getCurrentBid),
    path('add-onehund', views.addonehund),
    path('add-twohund', views.addtwohund),
    path('biddingbutton', views.biddingbutton),
    path('timecountdown', views.timecountdown),
    path('add-threehund', views.addthreehund),
    path('placeBid', views.placeBid, name='placeBid'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('support', views.support_action, name='support'),
    path('admin/', admin.site.urls),
    path('edit-profile', views.edit_profile_action, name='edit-profile'),
    path('payment/<int:id>/', include('LuxuryAuction.urls')),
    path('getproducts/<str:filter>', views.getProducts, name='getproducts'),
    path('searchproducts', views.searchProducts, name='searchproducts'),
]
