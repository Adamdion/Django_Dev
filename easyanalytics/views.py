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


# def transactions(request):
#     valid = False
#     """Renders the transactions page."""
#     # plot_div = ''
#     if request.method == 'POST' and request.FILES.get('file'):
#         # check if a file was uploaded
#         file = request.FILES['file']
#         # check if the file type is valid
#         if file.name.endswith('.csv') or file.name.endswith('.xls') or file.name.endswith('.xlsx'):
#             valid = True
#     elif request.method == 'POST' and request.POST['start_date'] and request.POST['end_date']:
#         # check if a file was uploaded
#         start_date = request.POST['start_date']
#         end_date = request.POST['end_date']
#         # check if the file type is valid
#         if start_date and end_date:
#             valid = True
#             # get the start and end dates from the form
#             plot_div = process_csv(file,start_date=request.POST['start_date'],end_date=request.POST['end_date'])
#             # generate the plot using the function in processors.py
#             return render(request, 'easyanalytics/transactions.html', {'title': 'Transactions', 'valid': valid,'plot_div': plot_div,})

#         else:
#             # invalid file type
#             error_msg = 'Invalid file type. Please upload a CSV or Excel file.'
#             plot_div = ''
#             return render(request, 'transactions.html', {'error_msg': error_msg})
    
#     else:
#         # no file uploaded
#         plot_div = ''
#     return render(request, 'easyanalytics/transactions.html', {'title': 'Transactions', 'valid': valid,'plot_div': plot_div,})
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