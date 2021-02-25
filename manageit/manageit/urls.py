"""manageit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as user_views

urlpatterns = [
    path('register/', user_views.register, name="accounts-register"),
    path('login/', user_views.user_login, name='accounts-login'),
    path('logout/', user_views.user_logout, name='accounts-logout'),
    path('account/', user_views.user_account, name='accounts-account'),
    path('', include('pages.urls')),
    path('projects/', include('projects.urls')),
    path('admin/', admin.site.urls),
    path('<str:ref_code>/', user_views.get_code, name='accounts-get-code'),
]
