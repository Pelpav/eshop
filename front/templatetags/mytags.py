from django import template

register = template.Library()

@register.filter
def set_get_param(value, param):
    param_name, param_val = param.split('=')
    if '?' not in value:
        return f"{value}?{param}"
    elif param_name not in value:
        return f"{value}&{param}"
    else:
        value_without_param, val = value.split(param_name + '=')
        uri = value_without_param + param
        if '&' in val:
            uri += "&".join(val.split('&')[1:])
        return uri
