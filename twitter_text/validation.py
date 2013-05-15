# encoding=utf-8

import re

from twitter_text.unicode import force_unicode
from twitter_text.extractor import Extractor
from twitter_text.regex import REGEXEN

MAX_LENGTH = 140

DEFAULT_TCO_URL_LENGTHS = {
  'short_url_length': 22,
  'short_url_length_https': 23,
  'characters_reserved_per_media': 22,
}

class Validation(object):
    def __init__(self, text, **kwargs):
        self.text = force_unicode(text)
        self.parent = kwargs.get('parent', False)
        
    def tweet_length(self, options = {}):
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

        for key in DEFAULT_TCO_URL_LENGTHS:
            if not key in options:
                options[key] = DEFAULT_TCO_URL_LENGTHS[key]

        length = len(self.text)
        # thanks force_unicode for making this so much simpler than the ruby version

        for url in Extractor(self.text).extract_urls_with_indices():
            # remove the link of the original URL
            length += url['indices'][0] - url['indices'][1]
            # add the length of the t.co URL that will replace it
            length += options.get('short_url_length_https') if url['url'].lower().find('https://') > -1 else options.get('short_url_length')

        if self.parent and hasattr(self.parent, 'tweet_length'):
            self.parent.tweet_length = length
        return length
    
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

        if not self.tweet_length():
            valid, validation_error = False, 'Empty text'

        if self.tweet_length() > MAX_LENGTH:
            valid, validation_error = False, 'Too long'

        if re.search(ur''.join(REGEXEN['invalid_control_characters']), self.text):
            valid, validation_error = False, 'Invalid characters'
            
        if self.parent and hasattr(self.parent, 'tweet_is_valid'):
            self.parent.tweet_is_valid = valid
        if self.parent and hasattr(self.parent, 'tweet_validation_error'):
            self.parent.tweet_validation_error = validation_error

        return validation_error if not valid else False

    def valid_tweet_text(self):
        return not self.tweet_invalid()

    def valid_username(self):
        if not self.text:
            return False

        extracted = Extractor(self.text).extract_mentioned_screen_names()

        return len(extracted) == 1 and extracted[0] == self.text[1:]

    def valid_list(self):
        match = re.compile(ur'^%s$' % REGEXEN['valid_mention_or_list'].pattern).search(self.text)
        return bool(match is not None and match.groups()[0] == "" and match.groups()[3])

    def valid_hashtag(self):
        if not self.text:
            return False

        extracted = Extractor(self.text).extract_hashtags()

        return len(extracted) == 1 and extracted[0] == self.text[1:]

    def valid_url(self, unicode_domains = True, require_protocol = True):
        if not self.text:
            return False

        url_parts = REGEXEN['validate_url_unencoded'].match(self.text)

        if not (url_parts and url_parts.string == self.text):
            return False

        scheme, authority, path, query, fragment = url_parts.groups()

        if not (
            (
                not require_protocol 
                or (
                    self._valid_match(scheme, REGEXEN['validate_url_scheme']) 
                    and re.compile(ur'^https?$', re.IGNORECASE).match(scheme)
                )
            )
            and (
                path == ''
                or self._valid_match(path, REGEXEN['validate_url_path'])
            )
            and self._valid_match(query, REGEXEN['validate_url_query'], True)
            and self._valid_match(fragment, REGEXEN['validate_url_fragment'], True)
        ):
            return False

        return bool(
            (
                unicode_domains 
                and self._valid_match(authority, REGEXEN['validate_url_unicode_authority'])
                and REGEXEN['validate_url_unicode_authority'].match(authority).string == authority
            )
            or (
                not unicode_domains
                and self._valid_match(authority, REGEXEN['validate_url_authority'])
                and REGEXEN['validate_url_authority'].match(authority).string == authority
            )
        )

    def _valid_match(self, string, re_obj, optional = False):
        if optional and string is None:
            return True
        match = re_obj.match(string)
        if optional:
            return not (string and (match is None or not match.string[match.span()[0]:match.span()[1]] == string))
        else:
            return bool(string and match and match.string[match.span()[0]:match.span()[1]] == string)
