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

import plotly.io as pio

def GrossProfitMargin(file):
    """Generate a cash flow report."""
    # read the file using pandas
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
        df = pd.read_excel(file)

     # Calculate gross profit margin
    df['gross_profit_margin'] = (df['Revenue'] - df['Expenses']) / df['Revenue']

    # Create plotly line chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Date'], y=df['gross_profit_margin'],
                        mode='lines', name='Gross Profit Margin'))
    fig.update_layout(title='Gross Profit Margin Over Time', xaxis_title='Date',
                      yaxis_title='Gross Profit Margin')
    fig = fig.to_json()
  
    # Calculate total change over the year for revenue, expenses, and profit

    profit_initial = df.loc[0, 'Profit']
    profit_final = df.loc[len(df)-1, 'Profit']
    profit_total_change = (profit_final - profit_initial) / profit_initial
   

    return fig, profit_total_change


def salesByProductReport(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    # Calculate total sales by product
    sales_by_product = df.groupby(df.iloc[:, 4])['Revenue'].sum().reset_index()


    # remake but use go instead of px
    # fig = go.Figure()
    # fig.add_trace(go.Pie(labels=sales_by_product.iloc[:,0], values=sales_by_product['Sales'])) 
    # fig.update_layout(title='Sales by Product')

    # Create a bar chart of sales by product
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=sales_by_product.iloc[:,0], y=sales_by_product.iloc[:,1]))
    fig_bar.update_layout(title='Sales by Product', xaxis_title='Product', yaxis_title='Revenue')
    # make plot look nicer
    fig_bar.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', 
                    marker_line_width=1.5, opacity=0.6)
                               

    # Calculate percentage of sales by product
    # total_sales = df['Sales'].sum()
    # sales_by_product['Percent'] = (sales_by_product['Sales'] / total_sales) * 100

    # Create a table of sales by product
    # fig_table = px.table(sales_by_product, title='Sales by Product', height=250)
    # write table using go
    fig_table = go.Figure(data=[go.Table(header=dict(values=list(sales_by_product.columns)),
                    cells=dict(values=[sales_by_product.iloc[:,0], sales_by_product.iloc[:,1]]))])
    fig_table.update_layout(title='Sales by Product')
    
    # Return the figures as a dictionary
    # figures = {'fig_pie': fig_pie, 'fig_bar': fig_bar, 'fig_table': fig_table}

    return [fig_bar.to_json(), fig_table.to_json()]



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