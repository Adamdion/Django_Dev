from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='easyanalytics-home'),
    path('about/', views.about, name='easyanalytics-about'),
    path('upload/', views.upload_file, name='upload_file'),
    path('transactions/', views.transactions, name='easyanalytics-transactions'),
    path('financial/', views.financial, name='easyanalytics-financial'),
    path('other/', views.other, name='easyanalytics-other'),
]