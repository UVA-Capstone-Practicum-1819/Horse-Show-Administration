from django.utils.safestring import mark_safe
from django.template import Library
from django.core import serializers
import json

register = Library()


@register.filter(is_safe=True)
def js(obj):
    # return mark_safe(json.dumps(obj))
    return serializers.serialize('json', obj)
