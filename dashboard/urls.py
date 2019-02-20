from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/', views.login, name="login"),
    url(r'logout/',views.logout, name="logout"),
    url(r'console/', views.console, name="console"),
    # url(r'create/', views.create, name="create"),
    url(r'create_scanner/', views.create_scanner, name="create_scanner"),

]
