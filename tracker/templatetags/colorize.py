from django.utils.safestring import mark_safe
from django import template
register = template.Library()


@register.filter
def colorize(value):
    mark = int(value)
    if mark < 0:
        html_string = f"<span style='color:green'>{mark}</span>"
    if mark > 0:
        html_string = f"<span style='color:red'>{mark}</span>"
    else:
        html_string = f"<span style='color:blue'>{mark}</span>"
    return mark_safe(html_string)
