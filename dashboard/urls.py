from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/', views.login, name="login"),
    url(r'logout/', views.logout, name="logout"),
    url(r'console/', views.console, name="console"),
    # url(r'create/', views.create, name="create"),
    url(r'create_scanner/', views.create_scanner, name="create_scanner"),
    url(r'scanner_list/', views.scanner_list, name="scanner_list"),
    url(r'search_log/', views.search_log, name="search_log"),
    url(r'search_log_api/', views.search_log_api, name="search_log_api"),
    url(r'search_log_del/', views.deletelog, name="search_log_del"),
]
