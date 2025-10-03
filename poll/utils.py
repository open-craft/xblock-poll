# -*- coding: utf-8 -*-
#
from gettext import translation as gnu_translation, NullTranslations
from bleach.sanitizer import Cleaner
from markdown import markdown

import pkg_resources
from django.utils.translation import get_language


# Make '_' a no-op so we can scrape strings
def _(text):
    return text


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


def get_xblock_i18n(runtime, fallback_domain="text"):
    """
    Get an i18n service for an XBlock.
    Will try runtime's service first, fallback to bundled GNU translations.
    """
    try:
        svc = runtime.service(None, "i18n")
        if svc and svc.ugettext("Thank you.") != "Thank you.":
            return svc
    except Exception:
        pass

    lang = get_language() or "en"
    locale_dir = pkg_resources.resource_filename(__name__, "translations")
    langs = [
        lang,
        lang.replace("-", "_"),
        lang.replace("_", "-"),
        lang.split("_")[0],
        lang.split("-")[0],
    ]
    try:
        g = gnu_translation(fallback_domain, localedir=locale_dir, languages=langs)
    except Exception:
        g = NullTranslations()

    class _I18N:
        def ugettext(self, s): return g.gettext(s)
        def ungettext(self, s, p, n): return g.ngettext(s, p, n)

    return _I18N()


def add_translations_to_studio_context(context, i18n):
    """
    Update the given context with all translatable strings
    used by Poll/Survey blocks.
    """
    context.update({
        "t_thanks": i18n.ugettext("Thank you."),
        "t_question_prompt": i18n.ugettext("Question/Prompt"),
        "t_enter_prompt_help": i18n.ugettext("Enter the prompt for the user."),
        # Markdown syntax support message with placeholders
        "t_markdown_supported": i18n.ugettext(
            "%(link_start)sMarkdown Syntax%(link_end)s is supported."
        ) % {
            'link_start': '<a href="https://daringfireball.net/projects/markdown/syntax" target="_blank">',
            'link_end': '</a>'
        },
        "t_extra_feedback": i18n.ugettext(
            "This text will be displayed for the user as some extra feedback after they have "
            "submitted their response to the poll."
        ),
        "t_private_results": i18n.ugettext("Private Results"),
        "t_set_private": i18n.ugettext("If this is set to True, don't display results of the poll to the user."),
        "t_max_submissions": i18n.ugettext("Maximum Submissions"),
        "t_max_submissions_help": i18n.ugettext(
            "Maximum number of times a user may submit a poll. %(bold_start)sSetting "
            "this to a value other than 1 will imply that 'Private Results' should be true."
            "%(bold_end)s Setting it to 0 will allow infinite resubmissions."
        ) % {
            'bold_start': '<strong>',
            'bold_end': '</strong>'
        },
        "t_notes": i18n.ugettext("Notes:"),
        "t_answer_change_warning": i18n.ugettext(
            "If you change an answer's text, all students who voted for that choice will have their votes "
            "updated to the new text. You'll want to avoid changing an answer from something like 'True' to "
            "'False', accordingly. If you delete an answer, any votes for that answer will also be deleted. "
            "Students whose choices are deleted may vote again, but will not lose course progress."
        ),
        "t_add_answer": i18n.ugettext("Add Answer"),
        "t_add_question": i18n.ugettext("Add Question"),
        "t_question_help": i18n.ugettext(
            "Questions must be similarly cared for. "
            "If a question's text is changed, any votes for that question will remain. "
            "If a question is deleted, any student who previously took the survey "
            "will be permitted to retake it, but will not "
            "lose course progress."
        ),
    })
    return context


def add_translations_to_student_context(context, i18n):
    """
    Update the given context with all translatable strings
    used by Poll/Survey blocks.
    """
    context.update({
            # Pass ALL translatable strings through context
            "t_submit": i18n.ugettext("Submit"),
            "t_thanks": i18n.ugettext("Thank you."),
            "t_export": i18n.ugettext("Export results to CSV"),
            "t_download": i18n.ugettext("Download CSV"),
            "t_vote": i18n.ugettext("Vote"),
            "t_view_results": i18n.ugettext("View results"),
            "t_total_votes": i18n.ugettext("Total votes"),
            # Add any other strings you need translated here
    })
    return context
