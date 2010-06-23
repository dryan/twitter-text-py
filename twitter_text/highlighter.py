# encoding=utf-8

import re

from twitter_text.regex import UNICODE_SPACES
from twitter_text.unicode import force_unicode

class HitHighlighter(object):

    DEFAULT_HIGHLIGHT_TAG = 'em'

    DEFAULT_HIGHLIGHT_CLASS = 'search-hit'
    
    def __init__(self, text, **kwargs):
        self.text = force_unicode(text)
        self.parent = kwargs.get('parent', False)

    def hit_highlight(self, query, **kwargs):
        """
        Add <em></em> tags around occurrences of query provided in the text except for occurrences inside of hashtags.
        
        The <em></em> tags can be overridden using the highlight_tag kwarg. For example:
        
        python> HitHighlighter('test hit here').hit_highlight(highlight_tag = 'strong', highlight_class = 'search-term')
                => "test <strong class='search-term'>hit</strong> here"
        """
        defaults = {
            'highlight_tag': kwargs.get('highlight_tag', self.DEFAULT_HIGHLIGHT_TAG).lower(),
            'highlight_class': kwargs.get('highlight_class', self.DEFAULT_HIGHLIGHT_CLASS).lower(),
        }
        kwargs.update(defaults)
        del(defaults)
        
        tags = ( u'<%s class="%s">' % ( kwargs.get('highlight_tag'), kwargs.get('highlight_class') ), u'</%s>' % kwargs.get('highlight_tag') )
        
        tag_search = re.compile(r'(<[^>]+>)')
        
        assert ( self.parent and not getattr(self.parent, 'has_been_linked', False) ) or tag_search.match(self.text), 'This text has already has HTML tags present. We can\'t highlight that reliably.' # make sure links have not already been run on this text
        del(tag_search)
        
        query_search = re.compile(ur'%s' % query, re.IGNORECASE)
        matches = query_search.finditer( self.text )
        wrapped_string = u'%s%s%s'
        UNICODE_SPACES.append(hex(20))
        len_diff = 0 # used to update the match offsets after the new wrapped text is inserted
        for match in matches:
            hashtag = False
            i = match.start() + len_diff - 1
            while i >= 0:
                if hex(ord(self.text[i])) in [hex(ord('#')), '0xff03']: # we don't want to wrap parts of hashtags as the link text will be wrong
                    hashtag = True
                    break
                elif hex(ord(self.text[i])) in UNICODE_SPACES:
                    break
                i -= 1
            if not hashtag:
                before = self.text[0:len_diff + match.start()]
                try:
                    after = self.text[len_diff + match.end():len(self.text)]
                except:
                    after = ''
                len_diff += len(before + wrapped_string % ( tags[0], match.group(0), tags[1] ) + after) - len(self.text)
                self.text = before + wrapped_string % ( tags[0], match.group(0), tags[1] ) + after

        del(query_search)
        del(matches)
        
        if self.parent and hasattr(self.parent, 'text'):
            self.parent.text = self.text
            
        del(tags)
        del(kwargs)
        
        return self.text