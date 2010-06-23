# encoding: utf-8

import re
from regex import REGEXEN

from twitter_text import force_unicode

class Autolink(object):
    
    WWW_REGEX = re.compile(r'www\.', re.IGNORECASE)

    DEFAULT_URL_CLASS = 'tweet-url'

    DEFAULT_LIST_CLASS = 'list-slug'

    DEFAULT_USERNAME_CLASS = 'username'

    DEFAULT_HASHTAG_CLASS = 'hashtag'

    HTML_ATTR_NO_FOLLOW = ' rel="nofollow"'

    def __init__(self, text, **kwargs):
        self.text = force_unicode(text)
        self.parent = kwargs.get('parent', False)

    def auto_link(self, **kwargs):
        """
        Add <a></a> tags around the usernames, lists, hashtags and URLs in the provided text. The
        <a> tags can be controlled with the following kwargs
    
        url_class::     class to add to all <a> tags
        list_class::    class to add to list <a> tags
        username_class::    class to add to username <a> tags
        hashtag_class::    class to add to hashtag <a> tags
        username_url_base::      the value for href attribute on username links. The @username (minus the @) will be appended at the end of this.
        list_url_base::      the value for href attribute on list links. The @username/list (minus the @) will be appended at the end of this.
        hashtag_url_base::      the value for href attribute on hashtag links. The #hashtag (minus the #) will be appended at the end of this.
        suppress_lists::    disable auto-linking to lists
        suppress_no_follow::   Do not add rel="nofollow" to auto-linked items
        html_attrs::    A dictionary of HTML attributes to add to non-Twitter URLS
        """
        self.auto_link_urls_custom(**kwargs.get('html_attrs', {}))
        self.auto_link_hashtags(**kwargs)
        self.auto_link_usernames_or_lists(**kwargs)

        if self.parent and hasattr(self.parent, 'text'):
            self.parent.text = self.text
        if self.parent and hasattr(self.parent, 'has_been_linked'):
            self.parent.has_been_linked = True

        return self.text
    
    def auto_link_usernames_or_lists(self, **kwargs):
        """
        Add <a></a> tags around the usernames and lists in the provided text. The
        <a> tags can be controlled with the following kwargs
    
        url_class::     class to add to all <a> tags
        list_class::    class to add to list <a> tags
        username_class::    class to add to username <a> tags
        username_url_base::      the value for href attribute on username links. The @username (minus the @) will be appended at the end of this.
        list_url_base::      the value for href attribute on list links. The @username/list (minus the @) will be appended at the end of this.
        suppress_lists::    disable auto-linking to lists
        suppress_no_follow::   Do not add rel="nofollow" to auto-linked items
        """
        defaults = {
            'url_class': self.DEFAULT_URL_CLASS,
            'list_class': self.DEFAULT_LIST_CLASS,
            'username_class': self.DEFAULT_USERNAME_CLASS,
            'username_url_base': 'http://twitter.com/',
            'list_url_base': 'http://twitter.com/',
        }
        kwargs.update(defaults)
        extra_html = kwargs.get('suppress_no_follow', False) or self.HTML_ATTR_NO_FOLLOW
    
        matches = REGEXEN['auto_link_usernames_or_lists'].finditer(self.text)
        for match in matches:
            _link = match.group(0)
            if match.group(4) is not None and not kwargs.get('suppress_lists', False):
                # this link is a list
                _list = u'%s%s' % (match.group(3), match.group(4))
                _link = u'%s%s<a class="%s" href="%s%s"%s>%s</a>' % ( match.group(1), match.group(2), ' '.join( [ kwargs.get('url_class', ''), kwargs.get('list_class', '') ] ), kwargs.get('list_url_base'), _list.lower(), extra_html, _list )
                del(_list)
            else:
                # this is a screen name
                _username = match.group(3)
                _link = u'%s<a class="%s" href="%s%s"%s>%s%s</a>' % ( match.group(1), ' '.join( [ kwargs.get('url_class'), kwargs.get('username_class', '') ] ), kwargs.get('username_url_base', ''), _username, extra_html, match.group(2), _username )
                del(_username)
            self.text = self.text.replace(match.group(0), _link)
            del(_link)

        if self.parent and hasattr(self.parent, 'text'):
            self.parent.text = self.text
        if self.parent and hasattr(self.parent, 'has_been_linked'):
            self.parent.has_been_linked = True

        del(matches)
        del(extra_html)
        del(kwargs)
        del(defaults)
        
        return self.text
    
    def auto_link_hashtags(self, **kwargs):
        """
        Add <a></a> tags around the hashtags in the provided text. The
        <a> tags can be controlled with the following kwargs
    
        url_class::     class to add to all <a> tags
        hashtag_class:: class to add to hashtag <a> tags
        hashtag_url_base::      the value for href attribute. The hashtag text (minus the #) will be appended at the end of this.
        suppress_no_follow::   Do not add rel="nofollow" to auto-linked items
        """
        defaults = {
            'url_class': self.DEFAULT_URL_CLASS,
            'hashtag_class': self.DEFAULT_HASHTAG_CLASS,
            'hashtag_url_base': 'http://twitter.com/search?q=%23',
        }
        kwargs.update(defaults)
        extra_html = kwargs.get('suppress_no_follow', False) or self.HTML_ATTR_NO_FOLLOW
    
        matches = REGEXEN['auto_link_hashtags'].finditer(self.text)
        for match in matches:
            _link = u'%s<a href="%s%s" title="#%s" class="%s"%s>%s%s</a>' % ( match.group(1), kwargs.get('hashtag_url_base'), match.group(3), match.group(3), ' '.join( [ kwargs.get('url_class', ''), kwargs.get('hashtag_class', '') ] ), extra_html, match.group(2), match.group(3) )
            self.text = self.text.replace(match.group(0), _link)

        if self.parent and hasattr(self.parent, 'text'):
            self.parent.text = self.text
        if self.parent and hasattr(self.parent, 'has_been_linked'):
            self.parent.has_been_linked = True

        del(matches)
        del(extra_html)
        del(kwargs)
        del(defaults)
        
        return self.text
    
    def auto_link_urls_custom(self, **kwargs):
        """
        Add <a></a> tags around the URLs in the provided text. Any
        elements in kwargs will be converted to HTML attributes
        and place in the <a> tag. Unless kwargs contains :suppress_no_follow
        the rel="nofollow" attribute will be added.
        """
        defaults = {}
        if kwargs.get('suppress_no_follow', False):
            del(kwargs['suppress_no_follow'])
        else:
            defaults = {
                'rel': ' '.join( [ kwargs.get('rel', ''), 'nofollow' ] )
            }

        html_attrs = []
        for k, v in kwargs.items():
            html_attrs = u'%s="%s"' % ( str(k), str(v) )
        html_attrs = ' '.join(html_attrs)
        if len(html_attrs):
            html_attrs = ' ' + html_attrs
        
        matches = REGEXEN['valid_url'].finditer(self.text)
        for match in matches:
            full_url = match.group(2)
            if match.group(3).find('http') == -1:
                full_url = u'http://%s' % full_url
            display_url = full_url
            if len(display_url) > 30:
                display_url = u'%s…' % display_url[0:30]
            _link = '%s<a href="%s"%s>%s</a>' % ( match.group(1), full_url, html_attrs, display_url )
            self.text = self.text.replace(match.group(0), _link)
            del(_link)
            del(full_url)
            del(display_url)

        if self.parent and hasattr(self.parent, 'text'):
            self.parent.text = self.text
        if self.parent and hasattr(self.parent, 'has_been_linked'):
            self.parent.has_been_linked = True
    
        del(matches)
        del(html_attrs)
        del(kwargs)
        del(defaults)
    
        return self.text