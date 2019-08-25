from django import template
from django.contrib.auth.models import Group
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter('markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['extra']))
