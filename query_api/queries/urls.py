from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.redirect_home, name='blank'),
    path('home/', views.home, name='home'),
]
