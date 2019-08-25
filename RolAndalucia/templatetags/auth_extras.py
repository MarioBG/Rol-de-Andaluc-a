from django import template
from django.contrib.auth.models import Group
import markdown
from django import template
from django.utils.safestring import mark_safe
from RolAndalucia.Markdown.TablesCool import TableExtension

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter('markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['abbr','RolAndalucia.Markdown.TablesCool:TableExtension','attr_list','def_list','fenced_code','footnotes','mdx_wikilink_plus']))
