"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from . import views
from moments.views.moment_views import main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('moments/', include('moments.urls')),
    path('pages/moments/', include('moments.pages_urls', namespace='moments')), # 페이지 렌더는 pages/로 시작!
    path('main/', main, name='main'), 
]

