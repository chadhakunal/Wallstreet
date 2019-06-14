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
app_name='bazaar'
urlpatterns = [
    path('register/',views.Register.as_view(),name='register'),
    path('', views.Login.as_view()),
    path('index/',views.postlogin.as_view(),name='index'),
    path('logoff/',views.Logoff,name='logoff'),
    path('company/',views.Company.as_view(),name='company'),
    path('buy/',views.Buy.as_view(),name='buy'),
    path('sell/',views.Sell.as_view(),name='sell'),
    path('news/',views.News.as_view(),name='news'),
    path('transactions/',views.Transactions.as_view(),name='transactions'),
    path('leaderboard/',views.LeaderBoard.as_view(),name='leaderboard'),


]
