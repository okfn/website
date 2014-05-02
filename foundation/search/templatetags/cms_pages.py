from django import template
from cms.models.pluginmodel import CMSPlugin
from cms.models.placeholdermodel import Placeholder

from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def placeholder_content(page, slot='blurb'):
    result = ''

    try:
        page_placeholders = page.placeholders.get(slot=slot)
    except Placeholder.DoesNotExist:
        return result
    for plugin in CMSPlugin.objects.filter(placeholder=page_placeholders):
        instance, plugin_type = plugin.get_plugin_instance()
        if instance is not None and hasattr(instance, 'body'):
            result += instance.body

    return mark_safe(result)
