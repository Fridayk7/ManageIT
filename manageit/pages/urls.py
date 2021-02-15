from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='pages-home'),
    path('account/', views.account, name='pages-account'),
    path('notifications/', views.notifications, name='pages-notifications'),
]
