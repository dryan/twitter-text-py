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

    def remove_overlapping_entities(self, entities):
        """
        Remove overlapping entities.
        This returns a new list with no overlapping entities.
        """

        # sort by start index
        entities.sort(key = lambda entity: entity['indices'][0])

        # remove duplicates
        prev    =   None
        for entity in [e for e in entities]:
            if prev and prev['indices'][1] > entity['indices'][0]:
                entities.remove(entity)
            prev    =   entity
        return entities

    def extract_entities_with_indices(self, options = {}, transform = lambda x: x):
        """
        Extracts all usernames, lists, hashtags and URLs  in the Tweet text
        along with the indices for where the entity ocurred
        If the text is None or contains no entity an empty list
        will be returned.

        If a transform is given then it will be called for each entity.
        """
        if not self.text:
            return []

        # extract all entities
        entities    =   self.extract_urls_with_indices(options) + \
                        self.extract_hashtags_with_indices({'check_url_overlap': False}) + \
                        self.extract_mentions_or_lists_with_indices() + \
                        self.extract_cashtags_with_indices()

        entities    =   self.remove_overlapping_entities(entities)

        for entity in entities:
            entity  =   transform(entity)

        return entities

    def extract_mentioned_screen_names(self, transform = lambda x: x):
        """
        Extracts a list of all usernames mentioned in the Tweet text. If the
        text is None or contains no username mentions an empty list
        will be returned.

        If a transform is given then it will be called for each username.
        """
        return [transform(mention['screen_name']) for mention in self.extract_mentioned_screen_names_with_indices()]

    def extract_mentioned_screen_names_with_indices(self, transform = lambda x: x):
        """
        Extracts a list of all usernames mentioned in the Tweet text
        along with the indices for where the mention ocurred.  If the
        text is None or contains no username mentions, an empty list
        will be returned.

        If a transform is given, then it will be called with each username, the start
        index, and the end index in the text.
        """
        if not self.text:
            return []

        possible_screen_names = []
        for match in self.extract_mentions_or_lists_with_indices():
            if not match['list_slug']:
                possible_screen_names.append({
                    'screen_name':  transform(match['screen_name']),
                    'indices':      match['indices']
                })
        return possible_screen_names

    def extract_mentions_or_lists_with_indices(self, transform = lambda x: x):
        """
        Extracts a list of all usernames or lists mentioned in the Tweet text
        along with the indices for where the mention ocurred.  If the
        text is None or contains no username or list mentions, an empty list
        will be returned.

        If a transform is given, then it will be called with each username, list slug, the start
        index, and the end index in the text. The list_slug will be an empty stirng
        if this is a username mention.
        """
        if not REGEXEN['at_signs'].search(self.text):
            return []

        possible_entries    =   []
        for match in REGEXEN['valid_mention_or_list'].finditer(self.text):
            try:
                after = self.text[match.end()]
            except IndexError:
                # the mention was the last character in the string
                after = None
            if after and REGEXEN['end_mention_match'].match(after) or match.groups()[2].find('http') == 0:
                continue
            possible_entries.append({
                'screen_name':  transform(match.groups()[2]),
                'list_slug':    match.groups()[3] or '',
                'indices':      [match.start() + len(match.groups()[0]), match.end()]
            })

        return possible_entries
        
    def extract_reply_screen_name(self, transform = lambda x: x):
        """
        Extracts the username username replied to in the Tweet text. If the
        text is None or is not a reply None will be returned.

        If a transform is given then it will be called with the username replied to (if any)
        """
        if not self.text:
            return None

        possible_screen_name = REGEXEN['valid_reply'].match(self.text)
        if possible_screen_name is not None:
            if possible_screen_name.group(1).find('http') > -1:
                possible_screen_name = None
            else:
                possible_screen_name = transform(possible_screen_name.group(1))
        return possible_screen_name
        
    def extract_urls(self, transform = lambda x: x):
        """
        Extracts a list of all URLs included in the Tweet text. If the
        text is None or contains no URLs an empty list
        will be returned.

        If a transform is given then it will be called for each URL.
        """
        return [transform(url['url']) for url in self.extract_urls_with_indices()]
        
    def extract_urls_with_indices(self, options = {'extract_url_without_protocol': True}):
        """
        Extracts a list of all URLs included in the Tweet text along
        with the indices. If the text is None or contains no
        URLs an empty list will be returned.

        If a block is given then it will be called for each URL.
        """
        urls = []
        for match in REGEXEN['valid_url'].finditer(self.text):
            complete, before, url, protocol, domain, port, path, query = match.groups()
            start_position = match.start() + len(before or '')
            end_position = match.end()
            # If protocol is missing and domain contains non-ASCII characters,
            # extract ASCII-only domains.
            if not protocol:
                if not options.get('extract_url_without_protocol') or REGEXEN['invalid_url_without_protocol_preceding_chars'].search(before):
                    continue
                last_url = None
                last_url_invalid_match = None
                for ascii_domain in REGEXEN['valid_ascii_domain'].finditer(domain):
                    ascii_domain = ascii_domain.group()
                    last_url = {
                        'url':      ascii_domain,
                        'indices':  [start_position - len(before or '') + complete.find(ascii_domain), start_position - len(before or '') + complete.find(ascii_domain) + len(ascii_domain)]
                    }
                    last_url_invalid_match = REGEXEN['invalid_short_domain'].search(ascii_domain) is not None
                    if not last_url_invalid_match:
                        urls.append(last_url)
                # no ASCII-only domain found. Skip the entire URL
                if not last_url:
                    continue
                if path:
                    last_url['url'] = url.replace(domain, last_url['url'])
                    last_url['indices'][1] = end_position
                    if last_url_invalid_match:
                        urls.append(last_url)
            else:
                if REGEXEN['valid_tco_url'].match(url):
                    url = REGEXEN['valid_tco_url'].match(url).group()
                    end_position = start_position + len(url)
                urls.append({
                    'url':      url,
                    'indices':  [start_position, end_position]
                })
        return urls
        
    def extract_hashtags(self, transform = lambda x: x):
        """
        Extracts a list of all hashtags included in the Tweet text. If the
        text is None or contains no hashtags an empty list
        will be returned. The list returned will not include the leading #
        character.

        If a block is given then it will be called for each hashtag.
        """
        return [transform(hashtag['hashtag']) for hashtag in self.extract_hashtags_with_indices()]
        
    def extract_hashtags_with_indices(self, options = {'check_url_overlap': True}, transform = lambda x: x):
        """
        Extracts a list of all hashtags included in the Tweet text. If the
        text is None or contains no hashtags an empty list
        will be returned. The list returned will not include the leading #
        character.

        If a block is given then it will be called for each hashtag.
        """
        tags = []
        for match in REGEXEN['valid_hashtag'].finditer(self.text):
            before, hashchar, hashtext = match.groups()
            start_position, end_position = match.span()
            start_position = start_position + len(before)
            if not (REGEXEN['end_hashtag_match'].match(self.text[end_position]) if len(self.text) > end_position else None) and not hashtext.find('http') == 0:
                tags.append({
                    'hashtag':  hashtext,
                    'indices':  [start_position, end_position]
                })

        if options.get('check_url_overlap'):
            urls = self.extract_urls_with_indices()
            if len(urls):
                tags = tags + urls
                # remove duplicates
                tags = self.remove_overlapping_entities(tags)
                tags = [tag for tag in tags if 'hashtag' in tag]

        return tags

    def extract_cashtags(self, transform = lambda x: x):
        """
        Extracts a list of all cashtags included in the Tweet text. If the
        text is None or contains no cashtags an empty list
        will be returned. The list returned will not include the leading $
        character.

        If a block is given then it will be called for each cashtag.
        """
        return [cashtag['cashtag'] for cashtag in self.extract_cashtags_with_indices()]

    def extract_cashtags_with_indices(self, transform = lambda x: x):
        """
        Extracts a list of all cashtags included in the Tweet text. If the
        text is None or contains no cashtags an empty list
        will be returned. The list returned will not include the leading $
        character.

        If a block is given then it will be called for each cashtag.
        """
        if not self.text or self.text.find('$') == -1:
            return []

        tags = []
        for match in REGEXEN['valid_cashtag'].finditer(self.text):
            before, dollar, cashtext = match.groups()
            start_position, end_position = match.span()
            start_position = start_position + len(before or '')
            tags.append({
                'cashtag':  cashtext,
                'indices':  [start_position, end_position]
            })

        return tags