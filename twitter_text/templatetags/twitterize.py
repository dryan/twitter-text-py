try:
    from django.template import Library
    from django.template.defaultfilters import stringfilter
except:
    raise Exception('Django is not installed.')

from twitter_text import TwitterText

register = Library()

@register.filter(name = 'twitter_text')
@stringfilter
def twitter_text(text, search_query = False):
    """
    Parses a text string through the TwitterText auto_link method and if search_query is passed, through the hit_highlight method.
    """
    tt = TwitterText(text)
    if search_query:
        tt.text     =   tt.highlighter.hit_highlight(query = search_query)
    tt.text         =   tt.autolink.auto_link()
    return tt.text
twitter_text.is_safe = True