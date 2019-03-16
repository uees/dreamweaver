from django.core.cache import cache

from .models import Option


def options_processor(requests):
    key = 'sar_cache'
    value = cache.get(key)
    if value:
        return value

    value = {}
    options = Option.objects.filter(enable=True).all()
    for option in options:
        value[option.slug] = option.value

    cache.set(key, value, 60 * 60 * 10)

    return value
