from django import template
from datetime  import datetime, timedelta

register = template.Library()

@register.filter(name='date_format')
def date_format(value, format_string):
    print("value: ", value)
    return datetime.strptime(value, '%Y-%m-%d').strftime('%B %d, %Y')

@register.filter(name='subtract_days')
def subtract_days(date, days):
    date = datetime.strptime(date, '%Y-%m-%d')
    new_date = date - timedelta(days=days)
    print("new_date: ", new_date)
    return new_date.strftime('%Y-%m-%d')