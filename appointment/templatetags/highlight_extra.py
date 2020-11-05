from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, keyword):
    highlighted = text.replace(keyword, '<span style="background-color: #FFFF00">{}</span>'.format(keyword))
    return mark_safe(highlighted)