"""Wallstreet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from . import views

app_name = 'bazaar'
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(),name='login'),
    path('logoff/', views.Logoff, name='logoff'),
    path('', views.postlogin.as_view(), name='index'),
    path('company/', views.CompanyView.as_view(), name='company'),
    path('buy/', views.Buy.as_view(), name='buy'),
    path('sell/', views.Sell.as_view(), name='sell'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('transactions/', views.Transactions.as_view(), name='transactions'),
    path('leaderboard/', views.LeaderBoardView.as_view(), name='leaderboard'),
]
