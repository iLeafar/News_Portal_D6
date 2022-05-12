from django import template


register = template.Library()

censwords = ['война', 'ххх', 'НАТО', 'альянса']


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    for i in censwords:
        if i.find(value):
            value = value.replace(i[1::], "*" * len(i))
    return f'{value}'
