# -*- coding: utf-8 -*-
#
from markdown import markdown


# Make '_' a no-op so we can scrape strings
def _(text):
    return text


def ngettext_fallback(text_singular, text_plural, number):
    """ Dummy `ngettext` replacement to make string extraction tools scrape strings marked for translation """
    return text_singular if number == 1 else text_plural


def remove_html_tags(data):
    """ Remove html tags from provided data """
    try:
        from bleach.sanitizer import Cleaner
        cleaner = Cleaner(tags=[], strip=True)
    except ImportError:
        # Bleach <2.0 compatibility fix
        import bleach
        cleaner = bleach

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
