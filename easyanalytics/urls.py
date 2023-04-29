from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='easyanalytics-home'),
    path('about/', views.about, name='easyanalytics-about'),
    path('transactions/', views.transactions, name='easyanalytics-transactions'),
    path('financial/', views.financial, name='easyanalytics-financial'),
    path('grossProfitMargin/', views.grossProfitMargin, name='easyanalytics-grossProfitMargin'),
    path('salesByProduct/', views.salesByProduct, name='easyanalytics-salesByProduct'),
    path('other/', views.other, name='easyanalytics-other'),
    path('create_post/', views.create_post, name='easyanalytics-create_post'),

]