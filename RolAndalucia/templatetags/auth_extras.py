from django import template
from django.contrib.auth.models import Group
import markdown
from django import template
from django.utils.safestring import mark_safe
from RolAndalucia.Markdown.TablesCool import TableExtension
import re
from urllib.parse import urlunparse

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def build_url(urlo, base, end, url_whitespace):
    """ Build and return a valid url.

    Parameters
    ----------

    urlo            A ParseResult object returned by urlparse

    base            base_url from config

    end             end_url from config

    url_whitespace  url_whitespace from config

    """
    if not urlo.netloc:
        if not end:
            clean_target = re.sub(r'\s+', url_whitespace, urlo.path)
        else:
            clean_target = re.sub(r'\s+', url_whitespace, urlo.path.rstrip('/'))
            if clean_target.endswith(end):
                end = ''
        if base.endswith('/'):
            path = "%s%s%s" % (base, clean_target.lstrip('/'), end)
        else:
            path = "%s%s%s" % (base, clean_target, end)
        urlo = urlo._replace(path=path)
    return urlunparse(urlo)


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter('markdown')
def markdown_format(text):
    md_configs = {
        'mdx_wikilink_plus': {
            'base_url': '/searchName?q=',
            'url_whitespace': '_',
            'label_case': 'titlecase',
            'html_class': 'wikilink',
            'build_url': build_url, # A callable
            # all of the above config params are optional
        },
    }
    return mark_safe(markdown.markdown(text, extensions=['extra', 'abbr','RolAndalucia.Markdown.TablesCool:TableExtension','attr_list','def_list','fenced_code','footnotes','mdx_wikilink_plus'], extension_configs = md_configs))
