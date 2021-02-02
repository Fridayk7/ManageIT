from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='pages-home'),
    path('account/', views.account, name='pages-account'),
    path('activity/', views.activity, name='pages-activity'),
    path('notifications/', views.notifications, name='pages-notifications'),
    path('list/', views.list, name='pages-list'),
    path('kanban/', views.kanban, name='pages-kanban'),
    path('gantchart/', views.gantchart, name='pages-gantchart'),
    path('dashboard/', views.dashboard, name='pages-dashboard'),
]
