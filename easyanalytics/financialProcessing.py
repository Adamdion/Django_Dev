import plotly.graph_objs as go
import plotly.io as pio
import io
import datetime
import pandas as pd
from plotly.subplots import make_subplots


def financialProcessing(file, start_date=datetime.date.today() - datetime.timedelta(days=365), end_date=datetime.date.today()):
    """Process financial data and return a Plotly plot."""

    # read the file using pandas
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
        df = pd.read_excel(file)

    line_chart = lineChart(df)

    growth_percentage = growthPercentage(df)

    growth_chart = growthChart(df)

    return line_chart, growth_percentage, growth_chart

def lineChart(df):
    # Group the data by year and sum the values for each group
    # data = df.groupby(df.index.year).sum()
    

    # Create a line plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Sales'],
                             mode='lines+markers', name='Sales'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Profit'],
                             mode='lines+markers', name='Profit'))

    # Set the layout of the plot
    fig.update_layout(
        title='Sales and Profit by Year',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        legend=dict(x=0, y=1)
    )

    # Convert the plot to HTML format
    buffer = io.StringIO()
    pio.write_html(fig, buffer)

    # Return the HTML string
    return buffer.getvalue()

def growthPercentage(df):
    # Calculate the growth percentage
    growth = ((df['Sales'].iloc[-1] - df['Sales'].iloc[0]) / df['Sales'].iloc[0]) * 100

    # Format the growth percentage
    growth = round(growth, 2)
    growth = str(growth) + '%'

    # Return the growth percentage
    return growth


def growthChart(df):
    # Create a line plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Sales'],
                             mode='lines+markers', name='Sales'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Profit'],
                             mode='lines+markers', name='Profit'))

    # Set the layout of the plot
    fig.update_layout(
        title='Sales and Profit Growth',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        legend=dict(x=0, y=1)
    )

    # Convert the plot to HTML format
    buffer = io.StringIO()
    pio.write_html(fig, buffer)

    # Return the HTML string
    return buffer.getvalue()

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.io as pio

def CashFlowReport(file):
    """Generate a cash flow report."""
    # read the file using pandas
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    # Convert the data to a pandas DataFrame
    # df = pd.DataFrame(data, columns=["Date", "Sales", "Expenses", "Profit"])
    
    # # Convert the Date column to a datetime data type
    df["Date"] = pd.to_datetime(df["Date"])
    df['Month']=pd.to_datetime(df["Date"]).dt.month
    # # Calculate the monthly cash flow
    # cash_flow = df.groupby(pd.Grouper(key="Date", freq="M")).sum()
    cash_flow = df.groupby(pd.Grouper(key="Month"))#.sum()

    # # Calculate the monthly net cash flow (Sales - Expenses)
    # net_cash_flow = cash_flow["Sales"] - cash_flow["Expenses"]

    # # Calculate the cumulative net cash flow
    # cumulative_net_cash_flow = net_cash_flow.cumsum()

    # # Calculate the percentage growth in net cash flow
    # pct_growth = cumulative_net_cash_flow.pct_change()

    # # Create a line chart of the monthly net cash flow with percentage growth
    # # make with go 
    # fig = go.Line(cumulative_net_cash_flow, title="Monthly Net Cash Flow with Percentage Growth")
    # fig = go.Scatter(pct_growth.index, pct_growth * 100, name="% Growth")
    # fig = go.Figure(data=fig)
    # fig2 = fig.to_json()

    # # Create a bar chart of the monthly sales and expenses
    # fig2 = [go.Bar(cash_flow, x=df['Date'], y=["Sales", "Expenses"], title="Monthly Sales and Expenses")]
    # fog2 = go.Bar({x=df['Date'], y=["Sales", "Expenses"], title="Monthly Sales and Expenses"})
    # fig2 = go.Figure(data=fig2)
    # fig2 = fig2.to_json()
    # Create a scatter plot of profit vs sales
    print("GETTOMG TP HERE")
    data = [go.Scatter(x=df['Sales'], y=df['Profit'])]
    print("GOT DATA")
    layout = go.Layout(title="Profit vs Sales", xaxis_title="Sales", yaxis_title="Profit")
    print("GOT layout")

    fig3 = go.Figure(data=data, layout=layout)
    fig3 = fig3.to_json()
  

    return fig3


def salesByProductReport(df):
    # Calculate total sales by product
    sales_by_product = df.groupby('Product')['Sales'].sum().reset_index()

    # Create a pie chart of sales by product
    fig_pie = px.pie(sales_by_product, values='Sales', names='Product', title='Sales by Product')

    # Create a bar chart of sales by product
    fig_bar = px.bar(sales_by_product, x='Product', y='Sales', title='Sales by Product')

    # Calculate percentage of sales by product
    total_sales = df['Sales'].sum()
    sales_by_product['Percent'] = (sales_by_product['Sales'] / total_sales) * 100

    # Create a table of sales by product
    fig_table = px.table(sales_by_product, title='Sales by Product', height=250)

    # Return the figures as a dictionary
    figures = {'fig_pie': fig_pie, 'fig_bar': fig_bar, 'fig_table': fig_table}

    return figures


def formatPlots(figures, title=None):
    rows = int(len(figures) / 2) + 1 if len(figures) % 2 != 0 else int(len(figures) / 2)
    fig = make_subplots(rows=rows, cols=2, vertical_spacing=0.3, horizontal_spacing=0.1)

    for i, f in enumerate(figures, start=1):
        row = int((i - 1) / 2) + 1
        col = i % 2 if i % 2 != 0 else 2

        for trace in f['data']:
            fig.add_trace(trace, row=row, col=col)

        fig.update_xaxes(title_text=f['layout']['xaxis']['title']['text'], row=row, col=col)
        fig.update_yaxes(title_text=f['layout']['yaxis']['title']['text'], row=row, col=col)

    fig.update_layout(showlegend=False, title=title)
    html_str = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return html_str