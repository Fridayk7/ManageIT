from django.urls import path, include
from . import views
from accounts import views as user_view

urlpatterns = [
    path('', views.home, name='projects'),
    path('createTask', views.create_task, name='createTask'),
    path('createWbs', views.create_wbs, name='createWbs'),
    path('createProject', views.create_project, name='createProject'),
    path('inviteTeam', views.invite_team, name='inviteTeam'),
    # path('goPremium', user_view.upgrade_to_premium, name='goPremium'),
    path('<int:project_id>', views.project, name='project'),
    path('<int:project_id>/', include('projectpages.urls')),
]
