# encoding=utf-8

from twitter_text.regex import REGEXEN
from twitter_text.unicode import force_unicode

class Extractor(object):
    """
    A module for including Tweet parsing in a class. This module provides function for the extraction and processing
    of usernames, lists, URLs and hashtags.
    """
    
    def __init__(self, text):
        self.text = force_unicode(text)
    
    def extract_mentioned_screen_names(self, transform = False):
        """
        Extracts a list of all usernames mentioned in the Tweet text. If the
        text contains no username mentions an empty list will be returned.
        
        If a transform is given, then it will be called with each username.
        """
        screen_names_only = []
        matches = self.extract_mentioned_screen_names_with_indices()
        for screen_name in matches:
            if transform:
                screen_name['screen_name'] = transform(screen_name['screen_name'])
            screen_names_only.append(screen_name['screen_name'])
            del(screen_name)
        del(matches)
        del(transform)
        return screen_names_only

    def extract_mentioned_screen_names_with_indices(self, transform = False):
        """
        Extracts a list of all usersnames mentioned in the Tweet text
        along with the indices for where the mention ocurred.  If the
        text contains no username mentions, an empty list will be returned.
        
        If a transform is given, then it will be called with each username, the start
        index, and the end index in the text.
        """
        possible_screen_names = []
        matches = REGEXEN['extract_mentions'].finditer(self.text)
        for match in matches:
            if transform:
                possible_screen_name = transform(match.group(0), match.start(), match.end())
            else:
                possible_screen_name = {
                    'screen_name': match.group(0),
                    'indicies': (match.start(), match.stop())
                }
            possible_screen_names.append(possible_screen_name)
            del(possible_screen_name)
        del(matches)
        del(transform)
        return possible_screen_names
        
    def extract_reply_screen_name(self, transform = False):
        """
        Extracts the first username replied to in the Tweet text. If the
        text does not contain a reply None will be returned.
        
        If a transform is given then it will be called with the username replied to (if any)
        """
        possible_screen_name = REGEXEN['extract_reply'].match(self.text).group(0)
        if transform:
            possible_screen_name = transform(possible_screen_name)
        del(transform)
        return possible_screen_name
        
    def extract_urls(self, transform = False):
        """
        Extracts a list of all URLs included in the Tweet text. If the
        text contains no URLs an empty list will be returned.
        
        If a transform is given then it will be called for each URL.
        """
        urls_only = []
        matches = self.extract_urls_with_indices()
        for url in matches:
            if transform:
                url['url'] = transform(url['url'])
            urls_only.append(url['url'])
            del(url)
        del(matches)
        del(transform)
        return urls_only
        
    def extract_urls_with_indices(self, transform = False):
        """
        Extracts a list of all URLs included in the Tweet text along
        with the indices. If the text contains no URLs an empty list
        will be returned.
        
        If a transform is given then it will be called for each URL.
        """
        urls = []
        matches = REGEXEN['valid_url'].finditer(self.text)
        for match in matches:
            if transform:
                url = transform(match.group(0), match.start(), match.end())
            else:
                url = {
                    'url': match.group(0),
                    'indices': (match.start(), match.stop())
                }
            urls.append(url)
            del(url)
        del(matches)
        del(transform)
        return urls
        
    def extract_hashtags(self, transform = False):
        """
        Extracts a list of all hashtags included in the Tweet text. If the
        text contains no hashtags an empty list will be returned.
        The list returned will not include the leading # character.
        
        If a transform is given then it will be called for each hashtag.
        """
        hashtags_only = []
        matches = self.extract_hashtags_with_indices()
        for hashtag in matches:
            if transform:
                hashtag['hashtag'] = transform(hashtag['hashtag'])
            hashtags_only.append(hashtag['hashtag'])
            del(hashtag)
        del(matches)
        del(transform)
        
        return hashtags_only
        
    def extract_hashtags_with_indices(self, transform = False):
        """
        Extracts a list of all hashtags included in the Tweet text. If the
        text contains no hashtags an empty list will be returned.
        The list returned will not include the leading # character.
        
        If a transform is given then it will be called for each hashtag.
        """
        tags = []
        matches = REGEXEN['auto_link_hashtags'].finditer(self.text)
        for match in matches:
            if transform:
                tag = transform(match.group(0), match.start(), match.end())
            else:
                tag = {
                    'hashtag': match.group(0),
                    'indices': (match.start(), match.stop())
                }
            tags.append(tag)
            del(tag)
        del(matches)
        del(transform)
        
        return tags