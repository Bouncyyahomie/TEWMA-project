from django import template


register = template.Library()

@register.filter
def iterator(lst, i):
    try:
        return lst[i]
    except:
        return None