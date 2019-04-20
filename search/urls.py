from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showresults/', views.results, name='results'),
    url(r'^result/ip/(?P<IP>[\S]*)$', views.result, name='result'),
]
