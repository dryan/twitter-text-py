# encoding = utf-8

import re

from twitter_text.unicode import force_unicode

class Validation(object):
    MAX_LENGTH = 140

    INVALID_CHARACTERS = (
        u'\uFFFE', u'\uFEFF',                                   # BOM
        u'\uFFFF',                                              # Special
        u'\u202A', u'\u202B', u'\u202C', u'\u202D', u'\u202E'   # Directional change
    )

    def __init__(self, text, **kwargs):
        self.text = force_unicode(text)
        self.parent = kwargs.get('parent', False)
        
    def tweet_length(self):
        """
        Returns the length of the string as it would be displayed. This is equivilent to the length of the Unicode NFC
        (See: http://www.unicode.org/reports/tr15). This is needed in order to consistently calculate the length of a
        string no matter which actual form was transmitted. For example:
        
            U+0065  Latin Small Letter E
        +   U+0301  Combining Acute Accent
        ----------
        =   2 bytes, 2 characters, displayed as é (1 visual glyph)
        … The NFC of {U+0065, U+0301} is {U+00E9}, which is a single chracter and a +display_length+ of 1
        
        The string could also contain U+00E9 already, in which case the canonicalization will not change the value.
        """

        assert (not self.parent or not getattr(self.parent, 'has_been_linked', False) ), 'The validator should only be run on text before it has been modified.'

        if self.parent and hasattr(self.parent, 'tweet_length'):
            self.parent.tweet_length = len(self.text)
        return len(self.text) # thanks force_unicode for making this so simple
    
    def tweet_invalid(self):
        """
        Check the text for any reason that it may not be valid as a Tweet. This is meant as a pre-validation
        before posting to api.twitter.com. There are several server-side reasons for Tweets to fail but this pre-validation
        will allow quicker feedback.
        
        Returns false if this text is valid. Otherwise one of the following Symbols will be returned:
        
            "Too long":: if the text is too long
            "Empty text":: if the text is empty
            "Invalid characters":: if the text contains non-Unicode or any of the disallowed Unicode characters
        """

        valid = True # optimism
        validation_error = None
        invalid_characters = re.compile(r'(%s)' % r'|'.join(self.INVALID_CHARACTERS), re.IGNORECASE)

        if not self.tweet_length():
            valid, validation_error = False, 'Empty text'
        if self.tweet_length() > self.MAX_LENGTH:
            valid, validation_error = False, 'Too long'
        if invalid_characters.match(self.text):
            valid, validation_error = False, 'Invalid characters'
            
        if self.parent and hasattr(self.parent, 'tweet_is_valid'):
            self.parent.tweet_is_valid = valid
        if self.parent and hasattr(self.parent, 'tweet_validation_error'):
            self.parent.tweet_validation_error = validation_error
            
        return (not valid, validation_error) # swap the valid value here to confirm to the original ruby version's API