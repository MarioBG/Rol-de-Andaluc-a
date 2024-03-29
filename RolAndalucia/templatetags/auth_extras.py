from django import template
from django.contrib.auth.models import Group
import markdown
from django import template
from django.utils.safestring import mark_safe
from RolAndalucia.Markdown.TablesCool import TableExtension
import re
from urllib.parse import urlunparse

register = template.Library()

@register.filter()
def range(min=5):
    return range(min)

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


@register.filter(name='replace_linebr')
def replace_linebr(value):
    """Replaces all values of line break from the given string with a line space."""
    return value.replace("\n", "<br />")


@register.filter('markdown')
def markdown_format(text):
    md_configs = {
        'RolAndalucia.Markdown.mdx_wikilink_plus:WikiLinkPlusExtension': {
            'configs': {'base_url': '/searchName?q=',
            'url_whitespace': '_',
            'label_case': 'titlecase',
            'html_class': 'wikilink',
            # all of the above config params are optional
        }

        },
    }
    return mark_safe(markdown.markdown(text, extensions=['extra', 'abbr','RolAndalucia.Markdown.TablesCool:TableExtension','attr_list','def_list','fenced_code','footnotes','RolAndalucia.Markdown.mdx_wikilink_plus:WikiLinkPlusExtension'], extension_configs = md_configs))


@register.filter('markdown_wiki')
def markdownwiki_format(text):
    md_configs = {
        'RolAndalucia.Markdown.mdx_wikilink_plus:WikiLinkPlusExtension': {
            'configs': {'base_url': '/searchWiki?q=',
            'url_whitespace': '_',
            'label_case': 'none',
            'html_class': 'wikilink',
            'is_wiki': 'T',
            # all of the above config params are optional
        }
        },
    }
    return mark_safe(markdown.markdown(text, extensions=['extra', 'abbr','RolAndalucia.Markdown.TablesCool:TableExtension','attr_list','def_list','fenced_code','footnotes','RolAndalucia.Markdown.mdx_wikilink_plus:WikiLinkPlusExtension'], extension_configs = md_configs))
