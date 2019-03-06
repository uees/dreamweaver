import logging

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


def options_processor(requests):
    key = 'sar_cache'
    value = cache.get(key)
    if value:
        return value

    logger.info('set sar cache.')
    value = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_SEO_DESCRIPTION': settings.SITE_DESCRIPTION,
        'SITE_DESCRIPTION': settings.SITE_DESCRIPTION,
        'SITE_BASE_URL': settings.SITE_URL,
    }
    cache.set(key, value, 60 * 60 * 10)

    return value
