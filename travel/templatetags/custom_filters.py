from django import template
import datetime

register = template.Library()

@register.filter
def to_kilometers(value):
    #Перевод м в км
    try:
        return float(value) / 1000.0
    except (ValueError, TypeError):
        return 0
    

@register.filter(name='format_seconds')
def format_seconds(value):
    try:
        total_seconds = int(value)
    except ValueError:  # если value не целое число, вернуть его как есть
        return value
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours}:{minutes:02d}"


MONTHS = {
    "01": "января", "02": "февраля", "03": "марта",
    "04": "апреля", "05": "мая", "06": "июня",
    "07": "июля", "08": "августа", "09": "сентября",
    "10": "октября", "11": "ноября", "12": "декабря",
}

@register.filter
def custom_date_format(value):
    if isinstance(value, datetime.date):
        return f"{value.day} {MONTHS[value.strftime('%m')]} {value.year}"
    return value