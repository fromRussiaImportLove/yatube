from django import template
from django.template.defaultfilters import stringfilter

"""
В template.Library зарегистрированы все теги и фильтры шаблонов
добавляем к ним и наш фильтры
"""

register = template.Library()


@register.filter
def addclass(field, css):
    """ Стоит разобраться, что это за фильтр """
    return field.as_widget(attrs={'class': css})


@register.filter
@stringfilter
def pluralized(value, forms):
    """
    Подбирает окончание существительному после числа
    {{someval|pluralize:"товар,товара,товаров"}}
    """
    try:
        one, two, many = forms.split(u',')
        value = str(value)

        if (21 > int(value) > 4):
            return value + ' ' + many

        if value.endswith('1'):
            return value + ' ' + one
        elif value.endswith(('2', '3', '4')):
            return value + ' ' + two
        else:
            return value + ' ' + many

    except (ValueError, TypeError):
        return ''
