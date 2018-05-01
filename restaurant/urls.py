
"""muypicky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.views.generic import TemplateView
from .views import (
        restaurant_listview,
        RestaurantListView, 
        SearchRestaurantListView,
        RestaurantDetailView,
        restaurant_createview,
        RestaurantCreateView,
        RestaurantUpdateView,
)


urlpatterns = [
    # url(r'^password_reset/', PasswordResetView.as_view(), name='password_reset'),    
    # url(r'^home/$', TemplateView.as_view(template_name='home.html'), name='home' ),
    # url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^$', RestaurantListView.as_view(), name='list'),
    url(r'^create/$', RestaurantCreateView.as_view(), name='create'),
    #url(r'^/create/$', restaurant_createview),
    url(r'^(?P<slug>[\w-]+)/edit$', RestaurantUpdateView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/$', RestaurantUpdateView.as_view(), name='detail'),
    #url(r'^(?P<slug>[\w-]+)/$', SearchRestaurantListView.as_view(), name='detail'),
    # url(r'^home3$', TemplateView.as_view(template_name='home3.html')),
    #url(r'^/(?P<slug>[\w-]+)/$', RestaurantDetailView.as_view()),
]