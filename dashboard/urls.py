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
    url(r'scanner_list_api/', views.scanner_list_api, name="scanner_list_api"),
    url(r'scanner/(?P<ID>[\S]*)', views.scanner, name="scanner"),
    url(r'scanner_oper/', views.scanner_oper, name="scanner_oper"),
    url(r'scanner_update/', views.scanner_update, name="scanner_update"),
    url(r'search_log/', views.search_log, name="search_log"),
    url(r'search_log_api/', views.search_log_api, name="search_log_api"),
    url(r'search_log_del/', views.deletelog, name="search_log_del"),
    url(r'create_scan_task/', views.create_scan_task, name="create_scan_task"),
]
