from django.contrib import admin
from django.urls import path, include
from login import views as login_views
from login.test_views import test_site


urlpatterns = [
    path("bobferguson/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/me/", login_views.me, name="me"),
    path("api/logout/", login_views.api_logout, name="api_logout"),
    path("", login_views.index, name="index"),
     path('test-site/', test_site),
    path("", include("login.urls")) 
]
