"""bitbid_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('User', views.signup),
    path('Seller', views.seller),
    path('Buyer', views.buyer),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('profile',views.profile),
    path('newItem',views.newItem),
    path('item/<id>/', views.bidView),
    path('newBid/<id>/', views.newBid),
    path('addMoney', views.addMoney),
    path('addRealMoney', views.addRealMoney),
    path('webhook/', views.coinbase_webhook)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
