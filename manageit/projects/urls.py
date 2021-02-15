from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='projects'),
    path('createTask', views.create_task, name='createTask'),
    path('createWbs', views.create_wbs, name='createWbs'),
    path('createProject', views.create_project, name='createProject'),
    path('<int:project_id>', views.project, name='project'),
    path('<int:project_id>/', include('projectpages.urls')),
]
