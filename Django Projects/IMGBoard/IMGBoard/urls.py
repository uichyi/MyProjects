"""
URL configuration for IMGBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from imageboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_login, name='landing'),
    path('rules/', views.show_rules, name='rules'),
    path('board/<str:board_id>/', views.board_page, name='board'),
    path('board/<str:board_id>/<int:thread_id>/', views.thread_page, name='thread'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('landing')), name='logout'),
    path('registration/', views.user_register, name='registration'),
    path('registration/success/', views.registration_success, name='success'),
    path('board/<str:board_id>/<int:thread_id>/remove', views.remove_thread, name='th_remove'),
    path('board/<str:board_id>/add', views.board_add, name='add_th'),
    path('board/<str:board_id>/<int:thread_id>/post', views.post_created, name='post_cr'),
    path('board/<str:board_id>/post', views.thread_created, name='post_th'),
    path('ajax/validate_username', views.validate_username, name='username_val'),
]
