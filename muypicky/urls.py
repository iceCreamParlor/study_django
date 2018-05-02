
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
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from django.views.generic import TemplateView
from django.contrib import admin

from profiles.views import ProfileFollowToggle, RegisterView, activate_user_view
from menus.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<code>[a-z0-9].*)', activate_user_view, name='activate'),


    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^password_reset/', PasswordResetView.as_view(), name='password_reset'),    
    url(r'^items/', include('menus.urls', namespace='menus')),
    url(r'^restaurants/', include('restaurant.urls', namespace='restaurants')),
    url(r'^u/', include('profiles.urls', namespace='profile')),
    url(r'^follow/$', ProfileFollowToggle.as_view(), name='follow'),
]