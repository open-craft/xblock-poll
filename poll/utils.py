# -*- coding: utf-8 -*-
#
from bleach.sanitizer import Cleaner
from markdown import markdown

# Tags and attributes allowed in author-authored content (question, feedback and
# answer/question labels) after it has been rendered from Markdown to HTML. Any
# other markup is stripped so the rendered HTML is safe to emit directly into the
# page (via ``|safe`` in Django templates and ``{{{ }}}`` in Handlebars).
MARKDOWN_ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code', 'em',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li', 'ol',
    'p', 'pre', 'strong', 'sub', 'sup', 'u', 'ul',
]
MARKDOWN_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'title'],
}
# Only allow safe URL protocols, so e.g. ``javascript:`` links are dropped.
MARKDOWN_ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


# Make '_' a no-op so we can scrape strings
def _(text):
    return text


def render_markdown(data):
    """
    Render Markdown to HTML, then sanitize it against an allow-list of tags,
    attributes and protocols.

    Markdown allows raw HTML to pass through untouched, so its output must be
    sanitized before being rendered unescaped to prevent stored XSS from
    author-supplied content.
    """
    cleaner = Cleaner(
        tags=MARKDOWN_ALLOWED_TAGS,
        attributes=MARKDOWN_ALLOWED_ATTRIBUTES,
        protocols=MARKDOWN_ALLOWED_PROTOCOLS,
        strip=True,
    )
    return cleaner.clean(markdown(data))


def ngettext_fallback(text_singular, text_plural, number):
    """ Dummy `ngettext` replacement to make string extraction tools scrape strings marked for translation """
    return text_singular if number == 1 else text_plural


def remove_html_tags(data):
    """ Remove html tags from provided data """
    cleaner = Cleaner(tags=[], strip=True)
    return cleaner.clean(data)


def remove_markdown_and_html_tags(data):
    """ Remove both markdown and html tags from provided data """
    return remove_html_tags(markdown(data))


class DummyTranslationService(object):  # pylint: disable=bad-option-value
    """
    Dummy drop-in replacement for i18n XBlock service
    """
    _catalog = {}
    gettext = _
    ngettext = ngettext_fallback
