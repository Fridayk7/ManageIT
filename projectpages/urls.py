from django.urls import path
from . import views

urlpatterns = [
    path('activity/', views.activity, name='projectpages-activity'),
    path('list/', views.list, name='projectpages-list'),
    path('wbs_list/', views.wbs_list, name='projectpages-wbs_list'),
    path('wbs/', views.wbs, name='projectpages-wbs'),
    path('gantchart/', views.gantchart, name='projectpages-gantchart'),
    path('dashboard/', views.dashboard, name='projectpages-dashboard'),
    path('list/updateTask', views.update_task, name='updateTask'),
    path('list/deleteTask', views.delete_task, name='deleteTask'),
    path('wbs_list/updateTask', views.update_task, name='update_task'),
    path('wbs_list/deleteTask', views.delete_task, name='delete_task'),
    path('wbs/updateWbs', views.update_wbs, name='updateWbs'),
    path('wbs/deleteWbs', views.delete_wbs, name='deleteWbs'),

]
