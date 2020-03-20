# -*- coding: utf-8 -*-
#


# Make '_' a no-op so we can scrape strings
def _(text):
    return text


def ngettext_fallback(text_singular, text_plural, number):
    """ Dummy `ngettext` replacement to make string extraction tools scrape strings marked for translation """
    return text_singular if number == 1 else text_plural


class DummyTranslationService(object):  # pylint: disable=bad-option-value
    """
    Dummy drop-in replacement for i18n XBlock service
    """
    _catalog = {}
    gettext = _
    ngettext = ngettext_fallback
