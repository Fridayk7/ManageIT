from django.urls import path
from . import views

urlpatterns = [
    path('activity/', views.activity, name='projectpages-activity'),
    path('list/', views.list, name='projectpages-list'),
    path('kanban/', views.kanban, name='projectpages-kanban'),
    path('gantchart/', views.gantchart, name='projectpages-gantchart'),
    path('dashboard/', views.dashboard, name='projectpages-dashboard'),
    ]