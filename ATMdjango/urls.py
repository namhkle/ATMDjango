"""DjangoATM URL Configuration

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
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from ATM import views


urlpatterns = [
    path('admin/', admin.site.urls), 
    #path('ATM/', index) for different pages
    path('', views.user_login),     # homepage
    path('user-account-panel/', views.user_account_panel), 
    path('admin-account-panel/', views.admin_account_panel), 
    path('admin-login/', views.admin_log_in), 
    path('admin-logout/', views.admin_log_out), 
   
    # only admin can view machines status, all accounts and all cards details. 
    path('atm-status/', views.atm_status), 
    path('admin-account-panel/card-details/', views.card_details),    
    path('admin-account-panel/account-details/', views.account_details), 

    # only user can have deposit, withdrawal, transfer and other features
    path('user-account-panel/card-details/', views.card_details),
    path('user-account-panel/deposit/', views.deposit),
    path('user-account-panel/withdrawal/', views.withdrawal),
    path('user-account-panel/transfer/', views.transfer),
    path('user-account-panel/block-card/', views.block_card),
    path('user-account-panel/activate-card/', views.activate_card),
    path('user-account-panel/reset-pin/', views.reset_pin),
    path('user-account-panel/update-phone/', views.update_phone),
    path('user-account-panel/update-expd/', views.update_expd),
    path('user-account-panel/view-history/', views.view_history),

    path('accounts/', include('django.contrib.auth.urls')),


]
