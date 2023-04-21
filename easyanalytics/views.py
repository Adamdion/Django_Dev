from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.core.files.storage import FileSystemStorage
from .processors import process_csv
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
def home(request):
    """Renders the home page."""
    return render(request, 'easyanalytics/home.html', context={})

def about(request):
    """Renders the about page."""
    return render(request, 'easyanalytics/about.html', {'title': 'About'})


import pandas as pd

def transactions(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
        except Exception as e:
            return render(request, 'easyanalytics/transactions.html', {'error': 'No file selected'})
        
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Load data from uploaded file
        # df = pd.read_csv(file)

        # # Filter data by date range
        # mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        # filtered_df = df.loc[mask]

        # Generate plot
        plot_div = process_csv(file,start_date=request.POST['start_date'],end_date=request.POST['end_date'])


        # Render plot image in HTML template
        return render(request, 'easyanalytics/transactions.html', {'plot_div': plot_div})
    else:
        return render(request, 'easyanalytics/transactions.html')
        

def financial(request):
    # ...code for handling financial analytics page...
    return render(request, 'easyanalytics/financial.html')

def other(request):
    # ...code for handling other analytics page...
    return render(request, 'easyanalytics/other.html')


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