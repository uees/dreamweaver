import json
import logging
import os

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.templatetags.static import static


logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def timeformat(data):
    try:
        return data.strftime(settings.TIME_FORMAT)
    except Exception as e:
        logger.error(e)
        return ""


@register.simple_tag
def datetimeformat(data):
    try:
        return data.strftime(settings.DATE_TIME_FORMAT)
    except Exception as e:
        logger.error(e)
        return ""


@register.simple_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)


@register.filter(is_safe=True)
@stringfilter
def truncate(content):
    from django.utils.html import strip_tags

    return strip_tags(content)[:150]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))


@register.simple_tag
def mix(type, path):
    manifest_path = os.path.join(settings.BASE_DIR, 'public/static/rev-manifest.json')

    if not os.path.isfile(manifest_path):
        raise Exception('The Mix manifest does not exist.')

    with open(manifest_path) as fp:
        manifest = json.load(fp)

    if not manifest.get(path):
        raise Exception("Unable to locate Mix file: {path}.".format(path=path))

    append_path = "{path}?id={hash}".format(
        path=static("{type}/{path}".format(type=type, path=path)),
        hash=manifest.get(path))

    return append_path
