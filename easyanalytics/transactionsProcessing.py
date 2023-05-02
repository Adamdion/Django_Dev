import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime


def process_csv(file, start_date=datetime.date.today() - datetime.timedelta(days=365), end_date=datetime.date.today()):
    """Process the uploaded csv file and return plotly plot
    
    Arguments:
        file {file} -- Uploaded csv file
            Date, Item, Cost
    """
    # read the file using pandas
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    # Convert columns to lowercase
    df.columns = df.columns.str.lower()
    # Get Figures
    fig1 = priceOverTime(df, start_date, end_date)
    fig2 = perItem(df, start_date, end_date)
    fig3 = perMonth(df, start_date, end_date)
    fig4 = totalSales(df, start_date, end_date)
    plot_div = formatPlots([fig1,fig2,fig3, fig4], title = "Transaction Analysis")
    return plot_div

# Create a line chart showing the price over time
def priceOverTime(df, start_date, end_date):
    """Create a line chart showing the price over time"""
    # create a line chart
    data = [go.Scatter(x=df['date'], y=df['cost'])]
    layout = go.Layout(title='Price Over Time', xaxis=dict(type='date'), yaxis={'title': 'Cost'})
    fig = go.Figure(data=data, layout=layout)
    return fig

# create a bar chart showing the amount spent on each item
def perItem(df, start_date, end_date):
    """Create a bar chart showing the amount spent on each item"""
    # create a new dataframe with the sum of the cost for each item
    df2 = df.groupby('item').sum()
    # create a bar chart
    data = [go.Bar(x=df2.index, y=df2['cost'])]
    # add x and y axis titles
    layout = go.Layout(title='Total Cost per Item', xaxis={'title': 'Item'}, yaxis={'title': 'Total Amount'})
    fig = go.Figure(data=data, layout=layout)
    return fig

# create a bar chart showing the amount spent per month
def perMonth(df, start_date, end_date):
    """Create a bar chart showing the amount spent per month"""
    # convert the date column to datetime
    df['month']=pd.to_datetime(df["date"]).dt.month
    # create a new dataframe with the sum of the cost for each month
    df = df.groupby('month').sum()
    # create a bar chart
    data = [go.Bar(x=df.index, y=df['cost'])]
    layout = go.Layout(title='Total Cost per Month', xaxis={'title': 'Month'}, yaxis={'title': 'Cost'})
    fig = go.Figure(data=data, layout=layout)
    return fig

# show the total sales as a number
def totalSales(df, start_date, end_date):
    """Show the total sales as a number"""
    # create a new dataframe with the sum of the cost for each month
    total = df['cost'].sum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0.5], y=[0.5], text=str(total), mode='text'))

    fig.update_xaxes(showgrid=False, visible=False)
    fig.update_yaxes(showgrid=False, visible=False)
    fig.update_layout(showlegend=False, font=dict(size=20), plot_bgcolor='white')

    return fig

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