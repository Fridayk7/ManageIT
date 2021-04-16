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
from pages import views as pages_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', user_views.register, name="accounts-register"),
    path('login/', user_views.user_login, name='accounts-login'),

    # https://www.youtube.com/watch?v=sFPcd6myZrY&list=RDCMUCTZRcDjjkVajGL6wd76UnGg&index=28
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

    path('logout/', user_views.user_logout, name='accounts-logout'),
    path('payment/', user_views.upgrade_to_premium, name='accounts-upgrade'),
    path('complete/', user_views.payment_complete, name='accounts-payment-complete'),
    path('', user_views.user_account, name='accounts-account'),
    path('notifications/', pages_views.notifications, name='notifications'),
    path('projects/', include('projects.urls')),
    path('admin/', admin.site.urls),
    path('<str:ref_code>.<str:project_code>/', user_views.get_code, name='accounts-get-code'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
