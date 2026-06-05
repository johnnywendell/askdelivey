from django import template
from django.templatetags.static import static
import hashlib
import os
from django.conf import settings

register = template.Library()

@register.simple_tag
def static_version(path):
    full_path = os.path.join(settings.STATIC_ROOT, path)
    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:6]
        return f"{static(path)}?v={file_hash}"
    return static(path)

@register.filter
def none_to_empty(value):
    return "" if value is None else value
