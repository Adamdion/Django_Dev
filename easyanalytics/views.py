from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post
from django.core.files.storage import FileSystemStorage
from .transactionsProcessing import process_csv
from .financialProcessing import financialProcessing, CashFlowReport, salesByProductReport
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse

import pandas as pd
import plotly.express as px

# Create your views here.
def home(request):
    """Renders the home page."""
    return render(request, 'easyanalytics/home.html', context={})

def about(request):
    """Renders the about page."""
    return render(request, 'easyanalytics/about.html', {'title': 'About'})



def transactions(request):
    """Renders the transactions page."""
    if request.method == 'POST':
        try:
            file = request.FILES['file']
        except Exception as e:
            return render(request, 'easyanalytics/transactions.html', {'error': 'No file selected'})

        plot_div = process_csv(file,start_date=request.POST['start_date'],end_date=request.POST['end_date'])


        # Render plot image in HTML template
        return render(request, 'easyanalytics/transactions.html', {'plot_div': plot_div})
    else:
        return render(request, 'easyanalytics/transactions.html')
        

# def financial(request):
#     """Renders the financial page."""
#     if request.method == 'POST':
#         try:
#             file = request.FILES['file']
#         except Exception as e:
#             return render(request, 'easyanalytics/transactions.html', {'error': 'No file selected'})

#         line_chart, growth_percentage, growth_chart = financialProcessing(file)
#         return render(request, 'easyanalytics/financial.html', {'line_chart': line_chart, 'growth_percentage': growth_percentage, 'growth_chart': growth_chart})
#     else: 
#         return render(request, 'easyanalytics/financial.html')

def financial(request):
    uploaded = False

    if request.method == 'POST':
        file = request.FILES['file']
        uploaded = True
        # Process the file here, e.g. save to disk, read data into DataFrame
        
        if 'cashflow' in request.POST:
            # Render the template for cash flow report with report data
            plot1 = CashFlowReport(file)
            print("Got to the cashflow report")
            request.session['plot1'] = plot1
            # request.session['plot1'] = plot2

            return redirect('easyanalytics-cashFlowReport')
        
        elif 'sales_by_product' in request.POST:
            # Call the sales by product report function and pass in the DataFrame
            report_data = salesByProductReport(file)
            
            # Render the template for sales by product report with report data
           
            return render(request, 'easyanalytics/sales_by_product_report.html', {'report_data': report_data})
        
        elif 'other_report' in request.POST:
            # Call another report function and pass in the DataFrame
            report_data = financialProcessing(file)
            
            # Render the template for the other report with report data
            return render(request, 'easyanalytics/other_report.html', {'report_data': report_data})
        
    # Render the template for the financial page if the request is GET
    return   render(request, 'easyanalytics/financial.html', {'uploaded': uploaded})



def other(request):
    return render(request, 'easyanalytics/other.html')

import plotly.graph_objs as go
import json
def cashFlowReport(request):
    """Renders the cashFlowReport page."""
    # Get the plotly figure from the session
    plot1 = request.session.get('plot1')
    # plot2 = request.session.get('plot2')

    # Convert the plotly figure to JSON
    fig_dict1 = json.loads(plot1)
    # fig_dict2 = json.loads(plot2)

    plot1 = go.Figure(fig_dict1)
    # plot2 = go.Figure(fig_dict2)
    plot1 = plot1.to_html(full_html=False)
    # plot2 = plot2.to_html(full_html=False)

    return render(request, 'easyanalytics/cashFlowReport.html', {'plot1': plot1})





# class FinancialView(View):
#     def get(self, request):
#         return render(request, 'financial.html')

#     def post(self, request):
#         if request.method == 'POST':
#             file = request.FILES['file']

#             # Determine which button was clicked
#             button_clicked = request.POST.get('action')

#             # Call appropriate function based on button clicked
#             if button_clicked == 'cash_flow_report':
#                 cash_flow_fig = self.cashFlowReport(file)
#                 cash_flow_fig.show()
#                 return render(request, 'financial.html')
#             elif button_clicked == 'transaction_report':
#                 transaction_fig = self.transaction(file)
#                 transaction_fig.show()
#                 return render(request, 'financial.html')
#             elif button_clicked == 'sales_by_product_report':
#                 sales_by_product_fig = self.salesByProduct(file)
#                 sales_by_product_fig.show()
#                 return render(request, 'financial.html')

#     def cashFlowReport(self,file):
#         """Generate a cash flow report."""
#         # read the file using pandas
#         if file.name.endswith('.csv'):
#             data = pd.read_csv(file)
#         elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
#             data = pd.read_excel(file)

#         # Convert the data to a pandas DataFrame
#         df = pd.DataFrame(data, columns=["Date", "Sales", "Expenses", "Profit"])

#         # Convert the Date column to a datetime data type
#         df["Date"] = pd.to_datetime(df["Date"])

#         # Calculate the monthly cash flow
#         cash_flow = df.groupby(pd.Grouper(key="Date", freq="M")).sum()

#         # Calculate the monthly net cash flow (Sales - Expenses)
#         net_cash_flow = cash_flow["Sales"] - cash_flow["Expenses"]

#         # Calculate the cumulative net cash flow
#         cumulative_net_cash_flow = net_cash_flow.cumsum()

#         # Calculate the percentage growth in net cash flow
#         pct_growth = cumulative_net_cash_flow.pct_change()

#         # Create a line chart of the monthly net cash flow with percentage growth
#         fig = px.line(cumulative_net_cash_flow, title="Monthly Net Cash Flow with Percentage Growth")
#         fig.add_scatter(x=pct_growth.index, y=pct_growth * 100, name="% Growth")

#         # Create a bar chart of the monthly sales and expenses
#         fig2 = px.bar(cash_flow, x=cash_flow.index, y=["Sales", "Expenses"], title="Monthly Sales and Expenses")

#         # Create a scatter plot of profit vs sales
#         fig3 = px.scatter(df, x="Sales", y="Profit", title="Profit vs Sales")

#         return [fig, fig2, fig3]

#     def transaction(self, data):
#         # Calculate transaction report
#         ...

#         # Create transaction chart using Plotly
#         ...

#         return transaction_fig

#     def salesByProduct(self, data):
#         # Calculate sales by product report
#         ...

#         # Create sales by product chart using Plotly
#         ...

#         return sales_by_product_fig