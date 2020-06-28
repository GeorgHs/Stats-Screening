from django import template

register = template.Library()


@register.filter
def in_list(value, the_list):
    value = str(value)
    str_list = ','.join(the_list)
    print(str_list)
    return value in str_list.split(',')


register.filter('in_list', in_list)
