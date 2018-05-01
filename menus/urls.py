from django.conf.urls import url, include

from .views import(
    ItemListView,
    ItemDetailView,
    ItemUpdateView,
    ItemCreateView,
    health_exercise,
    health_check,
)

urlpatterns = [
    url(r'^$', ItemListView.as_view(), name='list'),
    #url(r'^create/$', ItemCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/$', ItemDetailView.as_view(), name='detail'),
    url(r'^health_exercise/$', health_exercise),
    url(r'^health_check/$', health_check),


]