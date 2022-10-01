from django.conf import settings
from django import template

from form_builder.models import Fastq

register = template.Library()

# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

@register.simple_tag
def get_barcode_choices():
    return Fastq.barcode_choices