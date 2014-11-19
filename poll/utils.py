import bleach

from markdown import markdown


ALLOWED_TAGS = {
    'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': [],
    'a': ['target', 'href', 'class'], 'strong': [], 'em': [], 'blockquote': [],
    'pre': [], 'li': [], 'ul': [], 'ol': [], 'code': ['class'], 'p': [],
    }


def process_markdown(raw_text):
    return bleach.clean(markdown(raw_text), tags=ALLOWED_TAGS, strip_comments=False)