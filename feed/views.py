from django.shortcuts import render
from django.http import HttpResponse
# from .models import Post
from easyanalytics.models import Post

# this is the view for the home page
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'feed/home.html', context={'posts': posts})
