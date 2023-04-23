from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='easyanalytics-home'),
    path('about/', views.about, name='easyanalytics-about'),
    path('transactions/', views.transactions, name='easyanalytics-transactions'),
    path('financial/', views.financial, name='easyanalytics-financial'),
    path('cashFlowReport/', views.cashFlowReport, name='easyanalytics-cashFlowReport'),
    path('other/', views.other, name='easyanalytics-other'),
]