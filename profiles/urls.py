from django.conf.urls import url, include

from .views import(
    ProfileDetailView,
)

urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='detail'),
    
]