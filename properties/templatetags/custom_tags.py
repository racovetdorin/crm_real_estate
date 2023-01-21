import datetime
import textwrap

from dateutil.relativedelta import relativedelta
from django import template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from offers.models import Offer

from clients.models import Client

register = template.Library()


@register.filter
def sub_by_1(value):
    return value - 1 

@register.filter
def is_even(value):
    return value % 2 == 0


@register.filter
def division(value, arg):
    return value / arg


@register.filter
def floor_division(value, arg):
    if value and arg:
        return value // arg
    else:
        return None


@register.filter
def get_contract_end_date(value):
    return value + relativedelta(years=3)


@register.filter
def get_filter_name(value):
    return '_'.join(value.lower().split())


@register.filter
def get_image_hash(value):
    return value.strip('.jpeg').split('/')[-1]


@register.filter
def strip(value, arg):
    return value.strip(arg)


@register.filter
def to_empty_string(value):
    value = ""

    return value


@register.filter
def textwrap_string(value):
    return textwrap.fill(value, 40)


@register.filter
def append(value, element):
    return value.append(element)


@register.filter
def to_list(value):
    return list(value)


@register.filter
def join_lists(value, list):
    return value.extend(list)


@register.filter
def to_str(value):
    return str(value)


@register.filter
def list_to_str(value):
    return [str(x) for x in value]


@register.filter
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def blank_replace(value, arg):
    return value.replace(arg, ' ')


@register.filter
def concatenate(string):
    args = string.split()
    concatenated_string = ['' + arg for arg in args]

    return concatenated_string


@register.filter
def ends_with(value, arg):
    return value.endswith(arg)


@register.filter
def get_client_by_id(value):
    return Client.objects.filter(id=value).first()


@register.filter
def translate_bool(value):
    return _('Yes') if value else _("No")


@register.filter
def get_offer_by_id(value):
    return Offer.objects.filter(id=value).first()


@register.filter
def get(value, arg):
    return value.get(str(arg))


@register.filter
def date_subtraction(value, arg):
    if value and arg:
        delta = value - arg
        return delta.days

    return ''


@register.filter
def count_closed_offers(value):
    counter = 0
    for offer in value.offers.values():
        if offer.get('is_closed'):
            counter += 1

    return counter


@register.filter
def get_activity_ajax_search_id(activity, fk_object_field):
    fk_object_id = getattr(activity, fk_object_field + '_id')

    return f'activity-{activity.id}-{fk_object_field}-{fk_object_id}'


# SIMPLE TAGS

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.pop('page', None)
    query.update(kwargs)
    return query.urlencode()


@register.simple_tag()
def str_split(value, arg, get_element=False):
    if get_element:
        return value.split(arg)[get_element].title()
    return value.split(arg)
