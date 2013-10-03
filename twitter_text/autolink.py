# encoding=utf-8

import re, cgi

from twitter_text.regex import REGEXEN
from twitter_text.unicode import force_unicode
from twitter_text.extractor import Extractor

# Default CSS class for auto-linked lists
DEFAULT_LIST_CLASS = "tweet-url list-slug"
# Default CSS class for auto-linked usernames
DEFAULT_USERNAME_CLASS = "tweet-url username"
# Default CSS class for auto-linked hashtags
DEFAULT_HASHTAG_CLASS = "tweet-url hashtag"
# Default CSS class for auto-linked cashtags
DEFAULT_CASHTAG_CLASS = "tweet-url cashtag"

# Default URL base for auto-linked usernames
DEFAULT_USERNAME_URL_BASE = "https://twitter.com/"
# Default URL base for auto-linked lists
DEFAULT_LIST_URL_BASE = "https://twitter.com/"
# Default URL base for auto-linked hashtags
DEFAULT_HASHTAG_URL_BASE = "https://twitter.com/#!/search?q=%23"
# Default URL base for auto-linked cashtags
DEFAULT_CASHTAG_URL_BASE = "https://twitter.com/#!/search?q=%24"

# Default attributes for invisible span tag
DEFAULT_INVISIBLE_TAG_ATTRS = "style='position:absolute;left:-9999px;'"

DEFAULT_OPTIONS = {
  'list_class':             DEFAULT_LIST_CLASS,
  'username_class':         DEFAULT_USERNAME_CLASS,
  'hashtag_class':          DEFAULT_HASHTAG_CLASS,
  'cashtag_class':          DEFAULT_CASHTAG_CLASS,

  'username_url_base':      DEFAULT_USERNAME_URL_BASE,
  'list_url_base':          DEFAULT_LIST_URL_BASE,
  'hashtag_url_base':       DEFAULT_HASHTAG_URL_BASE,
  'cashtag_url_base':       DEFAULT_CASHTAG_URL_BASE,

  'invisible_tag_attrs':    DEFAULT_INVISIBLE_TAG_ATTRS,
}

OPTIONS_NOT_ATTRIBUTES = (
    'url_class',
    'list_class',
    'username_class',
    'hashtag_class',
    'cashtag_class',
    'username_url_base',
    'list_url_base',
    'hashtag_url_base',
    'cashtag_url_base',
    'username_url_transform',
    'list_url_transform',
    'hashtag_url_transform',
    'cashtag_url_transform',
    'link_url_transform',
    'username_include_symbol',
    'suppress_lists',
    'suppress_no_follow',
    'url_entities',
    'invisible_tag_attrs',
    'symbol_tag',
    'text_with_symbol_tag',
    'url_target',
    'link_attribute_transform',
    'link_text_transform',
)

HTML_ENTITIES = {
  '&': '&amp;',
  '>': '&gt;',
  '<': '&lt;',
  '"': '&quot;',
  "'": '&#39;',
}

BOOLEAN_ATTRIBUTES = (
    'disabled', 
    'readonly',
    'multiple',
    'checked',
)

def default_transform(entity, text):
    return text

class Autolink(object):
    def __init__(self, text, **kwargs):
        self.text = force_unicode(text)
        self.parent = kwargs.get('parent', False)
        self.extractor = Extractor(self.text)

    def auto_link_with_json(self, json_obj, options = {}):
        # concantenate entities
        entities = []
        if 'entities' in json_obj:
            json_obj = json_obj.get('entities')
        for key in json_obj:
            if type(json_obj[key]) == list:
                entities = entities + json_obj[key]

        # map JSON entity to twitter_text entity
        for entity in entities:
            if 'text' in entity:
                entity['hashtag'] = entity.get('text')

        return self.auto_link_entities(entities, options)

    def auto_link_entities(self, entities = [], options = {}):
        if not self.text:
            return self.text

        # NOTE deprecate these attributes not options keys in options hash, then use html_attrs
        options = dict(DEFAULT_OPTIONS.items() + options.items())
        options['html_attrs'] = self._extract_html_attrs_from_options(options)
        if not options.get('suppress_no_follow', False):
            options['html_attrs']['rel'] = "nofollow"

        entities.sort(key = lambda entity: entity['indices'][0], reverse = True)
        chars = self.text

        for entity in entities:
            if 'url' in entity:
                chars = self._link_to_url(entity, chars, options)
            elif 'hashtag' in entity:
                chars = self._link_to_hashtag(entity, chars, options)
            elif 'screen_name' in entity:
                chars = self._link_to_screen_name(entity, chars, options)
            elif 'cashtag' in entity:
                chars = self._link_to_cashtag(entity, chars, options)

        return chars

    def auto_link(self, options = {}):
        """
        Add <a></a> tags around the usernames, lists, hashtags and URLs in the provided text.
        The <a> tags can be controlled with the following entries in the options hash.
        Also any elements in the options hash will be converted to HTML attributes
        and place in the <a> tag.

        @url_class                  class to add to url <a> tags
        @list_class                 class to add to list <a> tags
        @username_class             class to add to username <a> tags
        @hashtag_class              class to add to hashtag <a> tags
        @cashtag_class              class to add to cashtag <a> tags
        @username_url_base          the value for href attribute on username links. The @username (minus the @) will be appended at the end of this.
        @list_url_base              the value for href attribute on list links. The @username/list (minus the @) will be appended at the end of this.
        @hashtag_url_base           the value for href attribute on hashtag links. The #hashtag (minus the #) will be appended at the end of this.
        @cashtag_url_base           the value for href attribute on cashtag links. The $cashtag (minus the $) will be appended at the end of this.
        @invisible_tag_attrs        HTML attribute to add to invisible span tags
        @username_include_symbol    place the @ symbol within username and list links
        @suppress_lists             disable auto-linking to lists
        @suppress_no_follow         do not add rel="nofollow" to auto-linked items
        @symbol_tag                 tag to apply around symbol (@, #, $) in username / hashtag / cashtag links
        @text_with_symbol_tag       tag to apply around text part in username / hashtag / cashtag links
        @url_target                 the value for target attribute on URL links.
        @link_attribute_transform   function to modify the attributes of a link based on the entity. called with |entity, attributes| params, and should modify the attributes hash.
        @link_text_transform        function to modify the text of a link based on the entity. called with (entity, text) params, and should return a modified text.
        """
        return self.auto_link_entities(self.extractor.extract_entities_with_indices({'extract_url_without_protocol': False}), options)

    def auto_link_usernames_or_lists(self, options = {}):
        """
        Add <a></a> tags around the usernames and lists in the provided text. The
        <a> tags can be controlled with the following entries in the options hash.
        Also any elements in the options hash will be converted to HTML attributes
        and place in the <a> tag.

        @list_class                 class to add to list <a> tags
        @username_class             class to add to username <a> tags
        @username_url_base          the value for href attribute on username links. The @username (minus the @) will be appended at the end of this.
        @list_url_base              the value for href attribute on list links. The @username/list (minus the @) will be appended at the end of this.
        @username_include_symbol    place the @ symbol within username and list links
        @suppress_lists             disable auto-linking to lists
        @suppress_no_follow         do not add rel="nofollow" to auto-linked items
        @symbol_tag                 tag to apply around symbol (@, #, $) in username / hashtag / cashtag links
        @text_with_symbol_tag       tag to apply around text part in username / hashtag / cashtag links
        @link_attribute_transform   function to modify the attributes of a link based on the entity. called with (entity, attributes) params, and should modify the attributes hash.
        @link_text_transform        function to modify the text of a link based on the entity. called with (entity, text) params, and should return a modified text.
        """
        return self.auto_link_entities(self.extractor.extract_mentions_or_lists_with_indices(), options)

    def auto_link_hashtags(self, options = {}):
        """
        Add <a></a> tags around the hashtags in the provided text.
        The <a> tags can be controlled with the following entries in the options hash.
        Also any elements in the options hash will be converted to HTML attributes
        and place in the <a> tag.

        @hashtag_class              class to add to hashtag <a> tags
        @hashtag_url_base           the value for href attribute. The hashtag text (minus the #) will be appended at the end of this.
        @suppress_no_follow         do not add rel="nofollow" to auto-linked items
        @symbol_tag                 tag to apply around symbol (@, #, $) in username / hashtag / cashtag links
        @text_with_symbol_tag       tag to apply around text part in username / hashtag / cashtag links
        @link_attribute_transform   function to modify the attributes of a link based on the entity. called with (entity, attributes) params, and should modify the attributes hash.
        @link_text_transform        function to modify the text of a link based on the entity. called with (entity, text) params, and should return a modified text.
        """
        return self.auto_link_entities(self.extractor.extract_hashtags_with_indices(), options)

    def auto_link_cashtags(self, options = {}):
        """
        Add <a></a> tags around the cashtags in the provided text.
        The <a> tags can be controlled with the following entries in the options hash.
        Also any elements in the options hash will be converted to HTML attributes
        and place in the <a> tag.

        @cashtag_class:: class to add to cashtag <a> tags
        @cashtag_url_base           the value for href attribute. The cashtag text (minus the $) will be appended at the end of this.
        @suppress_no_follow         do not add rel="nofollow" to auto-linked items
        @symbol_tag                 tag to apply around symbol (@, #, $) in username / hashtag / cashtag links
        @text_with_symbol_tag       tag to apply around text part in username / hashtag / cashtag links
        @link_attribute_transform   function to modify the attributes of a link based on the entity. called with (entity, attributes) params, and should modify the attributes hash.
        @link_text_transform        function to modify the text of a link based on the entity. called with (entity, text) params, and should return a modified text.
        """
        return self.auto_link_entities(self.extractor.extract_cashtags_with_indices(), options)

    def auto_link_urls(self, options = {}):
        """
        Add <a></a> tags around the URLs in the provided text.
        The <a> tags can be controlled with the following entries in the options hash.
        Also any elements in the options hash will be converted to HTML attributes
        and place in the <a> tag.

        @url_class                  class to add to url <a> tags
        @invisible_tag_attrs        HTML attribute to add to invisible span tags
        @suppress_no_follow         do not add rel="nofollow" to auto-linked items
        @symbol_tag                 tag to apply around symbol (@, #, $) in username / hashtag / cashtag links
        @text_with_symbol_tag       tag to apply around text part in username / hashtag / cashtag links
        @url_target                 the value for target attribute on URL links.
        @link_attribute_transform   function to modify the attributes of a link based on the entity. called with (entity, attributes) params, and should modify the attributes hash.
        @link_text_transform        function to modify the text of a link based on the entity. called with (entity, text) params, and should return a modified text.
        """
        return self.auto_link_entities(self.extractor.extract_urls_with_indices({'extract_url_without_protocol': False}), options)

    # begin private methods
    def _html_escape(self, text):
        for char in HTML_ENTITIES:
            text = text.replace(char, HTML_ENTITIES[char])
        return text

    def _extract_html_attrs_from_options(self, options = {}):
        html_attrs = options.get('html_attrs', {})
        options = options.copy()
        if 'html_attrs' in options:
            del(options['html_attrs'])
        for option in options.keys():
            if not option in OPTIONS_NOT_ATTRIBUTES:
                html_attrs[option] = options[option]
        return html_attrs

    def _url_entities_hash(self, url_entities):
        entities = {}
        for entity in url_entities:
            entities[entity.get('url')] = entity
        return entities

    def _link_to_url(self, entity, chars, options = {}):
        url = entity.get('url')

        href = options.get('link_url_transform', lambda x: x)(url)

        # NOTE auto link to urls do not use any default values and options
        # like url_class but use suppress_no_follow.
        html_attrs = self._extract_html_attrs_from_options(options)
        if options.get('url_class'):
            html_attrs['class'] = options.get('url_class')

        # add target attribute only if @url_target is specified
        if options.get('url_target'):
            html_attrs['target'] = options.get('url_target')

        url_entities = self._url_entities_hash(options.get('url_entities', {}))

        # use entity from @url_entities if available
        url_entity = url_entities.get(url, entity)
        if url_entity.get('display_url'):
            html_attrs['title'] = url_entity.get('expanded_url')
            link_text = self._link_url_with_entity(url_entity, options)
        else:
            link_text = self._html_escape(url)

        link = self._link_to_text(entity, link_text, href, html_attrs, options)
        return chars[:entity['indices'][0]] + link + chars[entity['indices'][1]:]

    def _link_url_with_entity(self, entity, options = {}):
        """
        Goal: If a user copies and pastes a tweet containing t.co'ed link, the resulting paste
        should contain the full original URL (expanded_url), not the display URL.

        Method: Whenever possible, we actually emit HTML that contains expanded_url, and use
        font-size:0 to hide those parts that should not be displayed (because they are not part of display_url).
        Elements with font-size:0 get copied even though they are not visible.
        Note that display:none doesn't work here. Elements with display:none don't get copied.

        Additionally, we want to *display* ellipses, but we don't want them copied.  To make this happen we
        wrap the ellipses in a tco-ellipsis class and provide an onCopy handler that sets display:none on
        everything with the tco-ellipsis class.

        Exception: pic.twitter.com images, for which expandedUrl = "https://twitter.com/#!/username/status/1234/photo/1
        For those URLs, display_url is not a substring of expanded_url, so we don't do anything special to render the elided parts.
        For a pic.twitter.com URL, the only elided part will be the "https://", so this is fine.
        """
        display_url = entity.get('display_url').decode('utf-8')
        expanded_url = entity.get('expanded_url')
        invisible_tag_attrs = options.get('invisible_tag_attrs', DEFAULT_INVISIBLE_TAG_ATTRS)

        display_url_sans_ellipses = re.sub(ur'…', u'', display_url)

        if expanded_url.find(display_url_sans_ellipses) > -1:
            before_display_url, after_display_url = expanded_url.split(display_url_sans_ellipses, 2)
            preceding_ellipsis = re.search(ur'\A…', display_url)
            following_ellipsis = re.search(ur'…\z', display_url)
            if preceding_ellipsis is not None:
                preceding_ellipsis = preceding_ellipsis.group()
            else:
                preceding_ellipsis = ''
            if following_ellipsis is not None:
                following_ellipsis = following_ellipsis.group()
            else:
                following_ellipsis = ''

            # As an example: The user tweets "hi http://longdomainname.com/foo"
            # This gets shortened to "hi http://t.co/xyzabc", with display_url = "…nname.com/foo"
            # This will get rendered as:
            # <span class='tco-ellipsis'> <!-- This stuff should get displayed but not copied -->
            #   …
            #   <!-- There's a chance the onCopy event handler might not fire. In case that happens,
            #        we include an &nbsp; here so that the … doesn't bump up against the URL and ruin it.
            #        The &nbsp; is inside the tco-ellipsis span so that when the onCopy handler *does*
            #        fire, it doesn't get copied.  Otherwise the copied text would have two spaces in a row,
            #        e.g. "hi  http://longdomainname.com/foo".
            #   <span style='font-size:0'>&nbsp;</span>
            # </span>
            # <span style='font-size:0'>  <!-- This stuff should get copied but not displayed -->
            #   http://longdomai
            # </span>
            # <span class='js-display-url'> <!-- This stuff should get displayed *and* copied -->
            #   nname.com/foo
            # </span>
            # <span class='tco-ellipsis'> <!-- This stuff should get displayed but not copied -->
            #   <span style='font-size:0'>&nbsp;</span>
            #   …
            # </span>

            return u"<span class='tco-ellipsis'>%s<span %s>&nbsp;</span></span><span %s>%s</span><span class='js-display-url'>%s</span><span %s>%s</span><span class='tco-ellipsis'><span %s>&nbsp;</span>%s</span>" % (preceding_ellipsis, invisible_tag_attrs, invisible_tag_attrs, self._html_escape(before_display_url), self._html_escape(display_url_sans_ellipses), invisible_tag_attrs, self._html_escape(after_display_url), invisible_tag_attrs, following_ellipsis)
        else:
            return self._html_escape(display_url)

    def _link_to_hashtag(self, entity, chars, options = {}):
        hashchar = chars[entity['indices'][0]]
        hashtag = entity['hashtag']
        hashtag_class = options.get('hashtag_class')

        if REGEXEN['rtl_chars'].search(hashtag):
            hashtag_class += ' rtl'

        href = options.get('hashtag_url_transform', lambda ht: u'%s%s' % (options.get('hashtag_url_base'), ht))(hashtag)

        html_attrs = {}
        html_attrs.update(options.get('html_attrs', {}))
        html_attrs = {
            'class':    hashtag_class,
            'title':    u'#%s' % hashtag,
        }

        link = self._link_to_text_with_symbol(entity, hashchar, hashtag, href, html_attrs, options)
        return chars[:entity['indices'][0]] + link + chars[entity['indices'][1]:]

    def _link_to_cashtag(self, entity, chars, options = {}):
        dollar = chars[entity['indices'][0]]
        cashtag = entity['cashtag']

        href = options.get('cashtag_url_transform', lambda ct: u'%s%s' % (options.get('cashtag_url_base'), ct))(cashtag)

        html_attrs = {
            'class': options.get('cashtag_class'),
            'title': u'$%s' % cashtag
        }
        html_attrs.update(options.get('html_attrs', {}))

        link = self._link_to_text_with_symbol(entity, dollar, cashtag, href, html_attrs, options)
        return chars[:entity['indices'][0]] + link + chars[entity['indices'][1]:]

    def _link_to_screen_name(self, entity, chars, options = {}):
        name = u'%s%s' % (entity['screen_name'], entity.get('list_slug') or '')
        chunk = options.get('link_text_transform', default_transform)(entity, name)
        name = name.lower()

        at = chars[entity['indices'][0]]

        html_attrs = options.get('html_attrs', {}).copy()
        if 'title' in html_attrs:
            del(html_attrs['title'])

        if entity.get('list_slug') and not options.get('supress_lists'):
            href = options.get('list_url_transform', lambda sn: u'%s%s' % (options.get('list_url_base'), sn))(name)
            html_attrs['class'] = options.get('list_class')
        else:
            href = options.get('username_url_transform', lambda sn: u'%s%s' % (options.get('username_url_base'), sn))(name)
            html_attrs['class'] = options.get('username_class')

        link = self._link_to_text_with_symbol(entity, at, chunk, href, html_attrs, options)
        return chars[:entity['indices'][0]] + link + chars[entity['indices'][1]:]

    def _link_to_text_with_symbol(self, entity, symbol, text, href, attributes = {}, options = {}):
        tagged_symbol = u'<%s>%s</%s>' % (options.get('symbol_tag'), symbol, options.get('symbol_tag')) if options.get('symbol_tag') else symbol
        text = self._html_escape(text)
        tagged_text = u'<%s>%s</%s>' % (options.get('text_with_symbol_tag'), text, options.get('text_with_symbol_tag')) if options.get('text_with_symbol_tag') else text
        if options.get('username_include_symbol') or not REGEXEN['at_signs'].match(symbol):
            return u'%s' % self._link_to_text(entity, tagged_symbol + tagged_text, href, attributes, options)
        else:
            return u'%s%s' % (tagged_symbol, self._link_to_text(entity, tagged_text, href, attributes, options))

    def _link_to_text(self, entity, text, href, attributes = {}, options = {}):
        attributes['href'] = href
        if options.get('link_attributes_transform'):
            attributes = options.get('link_attributes_transform')(entity, attributes)
        text = options.get('link_text_transform', default_transform)(entity, text)
        return u'<a %s>%s</a>' % (self._tag_attrs(attributes), text)

    def _tag_attrs(self, attributes = {}):
        attrs = []
        for key in sorted(attributes.keys()):
            value = attributes[key]
            if key in BOOLEAN_ATTRIBUTES:
                attrs.append(key)
                continue
            if type(value) == list:
                value = u' '.join(value)
            attrs.append(u'%s="%s"' % (self._html_escape(key), self._html_escape(value)))

        return u' '.join(attrs)