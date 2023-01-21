from django import template

register = template.Library()


@register.filter(name='query_params_from_dict')
def query_params_from_dict(request_dict):
    query_string = ''
    for key, value in request_dict.items():
        query_string += f'{key}={value}&'

    if query_string:
        return f'&{query_string}'
    return ''


@register.simple_tag(name='can_view_client_details')
def can_view_client_details(user, client, *args, **kwargs):
    return user.can_view_client_details(client)


@register.simple_tag(name='can_edit_client')
def can_edit_client(user, client, *args, **kwargs):
    return user.can_edit_client(client)


@register.simple_tag(name='can_delete_client')
def can_delete_client(user, client, *args, **kwargs):
    return user.can_delete_client(client)


@register.filter()
def to_int(value):
    return int(value)


@register.filter()
def to_str(value) -> str:
    return str(value)
