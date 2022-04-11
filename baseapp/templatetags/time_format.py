from django.template import Library
from datetime import datetime

register = Library()

@register.simple_tag
def time_format(datetime):
    return datetime.strftime("%d.%m.%Y")
