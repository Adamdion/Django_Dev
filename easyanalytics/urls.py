from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='easyanalytics-home'),
    path('about/', views.about, name='easyanalytics-about'),
    path('upload/', views.upload_file, name='upload_file')

]