from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.core.files.storage import FileSystemStorage
from .processors import process_csv
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
def home(request):
    """Renders the home page."""
    if request.method == 'POST' and request.FILES.get('file'):
        # check if a file was uploaded
        file = request.FILES['file']
        # check if the file type is valid
        if file.name.endswith('.csv') or file.name.endswith('.xls') or file.name.endswith('.xlsx'):
            # process the file using the function in processors.py
            plot_div = process_csv(file)
            # generate the plot using the function in processors.py
            # plot_div = generate_plot(data)
        else:
            # invalid file type
            error_msg = 'Invalid file type. Please upload a CSV or Excel file.'
            return render(request, 'home.html', {'error_msg': error_msg})
    else:
        # no file uploaded
        plot_div = ''
    return render(request, 'easyanalytics/home.html', context={'plot_div': plot_div,'posts': Post.objects.all()})

def about(request):
    """Renders the about page."""
    return render(request, 'easyanalytics/about.html', {'title': 'About'})

from .processors import process_csv

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        data = process_csv(uploaded_file)
        # process the data as needed
        return render(request, 'success.html')
    return render(request, 'upload.html')


###### From Tutorial to create, delete, update, and list posts

## if not a post format no use for this, can delete

# class PostListView(ListView):
#     model = Post
#     template_name = 'easyanalytics/home.html' # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5

# class PostDetailView(DetailView):
#     model = Post

# class PostCreateView(CreateView):
#     model = Post
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)