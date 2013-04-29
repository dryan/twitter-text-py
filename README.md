A port of the Ruby gem [twitter-text-rb](https://github.com/twitter/twitter-text-rb) to Python.

# Usage

You can either call a new TwitterText object with the text of the tweet you want to process `TwitterText('twitter-text-py is #awesome')` or use any of the submodule objects directly (Autolink, Extractor, HitHighlighter or Validation), passing in the tweet text as an argument.

The library also contains a Django template filter that applies the auto_link method to the passed in text. It can also optionally apply the hit_highlight method. Example:

    {% load twitterize %}

    {{ obj.body|twitter_text }} <!-- just add the links -->
    {{ obj.body|twitter_text:"my term" }} <!-- add the links and highlight the search term -->

You can test that the library is working correctly by running `python tests.py` inside the `twitter_text` directory.

## TwitterText(text)

### Properties:

* text:             the original text you passed in, or the modified version if you've called any functions on the object.
* original_text:    the original text you passed in; never modified. Useful for a fallback or to do comparisons.
* has_been_linked:  boolean denoting if any of the Autolink functions have been called. (Mostly for internal use.)
* tweet_length:     the value returned by `validation.tweet_length` or None if that function has not yet been called.
* tweet_is_valid:   boolean returned by `validation.tweet_invalid` or None if that function has not yet been called.
* validation_error: the validation error string returned by `validation.tweet_invalid` or None if that function has not yet been called.
* autolink:         property pointing to an Autolink object initialized with `text`
* extractor:        property pointing to an Extractor object initialized with `text`
* highlighter:      property pointing to a HitHighlighter object initialized with `text`
* validation:       property pointing to a Validation object initialized with `text`

## Autolink(text)

This object modifies the text passed to it (and the parent TwitterText.text if present).

### Defaults

These may be overridden by kwargs on a particular method.

* url_class         =   'tweet-url'
* list_class        =   'list-slug'
* username_class    =   'username'
* hashtag_class     =   'hashtag'

### Methods:

__auto_link(self, **kwargs)__

Add `<a></a>` tags around the usernames, lists, hashtags and URLs in the provided text. The `<a>` tags can be controlled with the following kwargs:

* url_class:            class to add to all `<a>` tags
* list_class:           class to add to list `<a>` tags
* username_class:       class to add to username `<a>` tags
* hashtag_class:        class to add to hashtag `<a>` tags
* username_url_base:    the value for href attribute on username links. The @username (minus the @) will be appended at the end of this.
* list_url_base:        the value for href attribute on list links. The @username/list (minus the @) will be appended at the end of this.
* hashtag_url_base:     the value for href attribute on hashtag links. The #hashtag (minus the #) will be appended at the end of this.
* suppress_lists:       disable auto-linking to lists
* suppress_no_follow:   do not add rel="nofollow" to auto-linked items
* html_attrs:           a dictionary of HTML attributes to add to non-Twitter links

__auto_link_usernames_or_lists(self, **kwargs)__

Add `<a></a>` tags around the usernames and lists in the provided text. The `<a>` tags can be controlled with the following kwargs:

* url_class:            class to add to all `<a>` tags
* list_class:           class to add to list `<a>` tags
* username_class:       class to add to username `<a>` tags
* username_url_base:    the value for href attribute on username links. The @username (minus the @) will be appended at the end of this.
* list_url_base:        the value for href attribute on list links. The @username/list (minus the @) will be appended at the end of this.
* suppress_lists:       disable auto-linking to lists
* suppress_no_follow:   do not add rel="nofollow" to auto-linked items

__auto_link_hashtags(self, **kwargs)__

Add `<a></a>` tags around the hashtags in the provided text. The `<a>` tags can be controlled with the following kwargs:

* url_class:            class to add to all `<a>` tags
* hashtag_class:        class to add to hashtag `<a>` tags
* hashtag_url_base:     the value for href attribute. The hashtag text (minus the #) will be appended at the end of this.
* suppress_no_follow:   do not add rel="nofollow" to auto-linked items

__auto_link_urls_custom(self, **kwargs)__

Add `<a></a>` tags around the URLs in the provided text. Any elements in kwargs (except @supress_no_follow@) will be converted to HTML attributes and place in the `<a>` tag. Unless kwargs contains @suppress_no_follow@ the rel="nofollow" attribute will be added.

## Extractor

This object does not modify the text passed to it (or the parent TwitterText.text if present).

### Methods

__extract_mentioned_screen_names__

Extracts a list of all usernames mentioned in the Tweet text. If the text contains no username mentions an empty list will be returned.

If a transform is given, then it will be called with each username.

__extract_mentioned_screen_names_with_indices__

Extracts a list of all usernames mentioned in the Tweet text along with the indices for where the mention occurred in the format:

    {
        'username': username_string,
        'indicies': ( start_postion, end_position )
    }

If the text contains no username mentions, an empty list will be returned.

If a transform is given, then it will be called with each username, the start index, and the end index in the text.

__extract_reply_screen_name__

Extracts the first username replied to in the Tweet text. If the text does not contain a reply None will be returned.

If a transform is given then it will be called with the username replied to (if any).

__extract_urls__

Extracts a list of all URLs included in the Tweet text. If the text contains no URLs an empty list will be returned.

If a transform is given then it will be called for each URL.

__extract_urls_with_indices__

Extracts a list of all URLs included in the Tweet text along with the indices in the format:

    {
        'url': url_string,
        'indices': ( start_postion, end_position )
    }

If the text contains no URLs an empty list will be returned.

If a transform is given then it will be called for each URL, the start index, and the end index in the text.

__extract_hashtags__

Extracts a list of all hashtags included in the Tweet text. If the text contains no hashtags an empty list will be returned. The list returned will not include the leading # character.

If a transform is given then it will be called for each hashtag.

__extract_hashtags_with_indices__

Extracts a list of all hashtags included in the Tweet text along with the indices in the format:

    {
        'hashtag': hashtag_text,
        'indices': ( start_postion, end_position )
    }

If the text contains no hashtags an empty list will be returned. The list returned will not include the leading # character.

If a transform is given then it will be called for each hashtag.

## HitHighlighter

### Defaults

These may be overridden by kwargs on a particular method.

* highlight_tag = 'em'
* highlight_class = 'search-hit'

### Methods

__hit_highlight(self, query, **kwargs)__

Add `<em></em>` tags around occurrences of query provided in the text except for occurrences inside hashtags.

The `<em></em>` tags or css class can be overridden using the highlight_tag and/or highlight_class kwarg. For example:

    python> HitHighlighter.hit_highlight('test hit here').hit_highlight('hit', highlight_tag = 'strong', highlight_class = 'search-term')
            =\> "test <strong class='search-term'>hit</strong> here"


## Validation

### Methods

__tweet_length__

Returns the length of the string as it would be displayed. This is equivilent to the length of the Unicode NFC (See: http://www.unicode.org/reports/tr15). This is needed in order to consistently calculate the length of a string no matter which actual form was transmitted. For example:

    U+0065 Latin Small Letter E
    + U+0301 Combining Acute Accent
    ----------
    = 2 bytes, 2 characters, displayed as é (1 visual glyph)

The NFC of {U+0065, U+0301} is {U+00E9}, which is a single character and a display length of 1

The string could also contain U+00E9 already, in which case the canonicalization will not change the value.

__tweet_invalid__

Check the text for any reason that it may not be valid as a Tweet. This is meant as a pre-validation before posting to api.twitter.com. There are several server-side reasons for Tweets to fail but this pre-validation will allow quicker feedback.

Returns false if this text is valid. Otherwise one of the following Symbols will be returned:

* "Too long": if the text is too long
* "Empty text": if the text is empty
* "Invalid characters": if the text contains non-Unicode or any of the disallowed Unicode characters
