#  encoding=utf-8

# A collection of regular expressions for parsing Tweet text. The regular expression
# list is frozen at load time to ensure immutability. These reular expressions are
# used throughout the Twitter classes. Special care has been taken to make
# sure these reular expressions work with Tweets in all languages.
import re, string

REGEXEN = {} # :nodoc:

def regex_range(start, end = None):
    if end:
        return u'%s-%s' % (unichr(start), unichr(end))
    else:
        return u'%s' % unichr(start)

# Space is more than %20, U+3000 for example is the full-width space used with Kanji. Provide a short-hand
# to access both the list of characters and a pattern suitible for use with String#split
#  Taken from: ActiveSupport::Multibyte::Handlers::UTF8Handler::UNICODE_WHITESPACE
UNICODE_SPACES = []
for space in reduce(lambda x,y: x + y if type(y) == list else x + [y], [
        range(0x0009, 0x000D),  # White_Space # Cc   [5] <control-0009>..<control-000D>
        0x0020,                 # White_Space # Zs       SPACE
        0x0085,                 # White_Space # Cc       <control-0085>
        0x00A0,                 # White_Space # Zs       NO-BREAK SPACE
        0x1680,                 # White_Space # Zs       OGHAM SPACE MARK
        0x180E,                 # White_Space # Zs       MONGOLIAN VOWEL SEPARATOR
        range(0x2000, 0x200A),  # White_Space # Zs  [11] EN QUAD..HAIR SPACE
        0x2028,                 # White_Space # Zl       LINE SEPARATOR
        0x2029,                 # White_Space # Zp       PARAGRAPH SEPARATOR
        0x202F,                 # White_Space # Zs       NARROW NO-BREAK SPACE
        0x205F,                 # White_Space # Zs       MEDIUM MATHEMATICAL SPACE
        0x3000,                 # White_Space # Zs       IDEOGRAPHIC SPACE
    ]):
    UNICODE_SPACES.append(unichr(space))
REGEXEN['spaces'] = re.compile(ur''.join(UNICODE_SPACES))

# Characters not allowed in Tweets
INVALID_CHARACTERS  =   [
    0xFFFE, 0xFEFF,                         # BOM
    0xFFFF,                                 # Special
    0x202A, 0x202B, 0x202C, 0x202D, 0x202E, # Directional change
]
REGEXEN['invalid_control_characters']   =   [unichr(x) for x in INVALID_CHARACTERS]

REGEXEN['list_name'] = re.compile(ur'^[a-zA-Z][a-zA-Z0-9_\-\u0080-\u00ff]{0,24}$')

# Latin accented characters
# Excludes 0xd7 from the range (the multiplication sign, confusable with "x").
# Also excludes 0xf7, the division sign
LATIN_ACCENTS = [
    regex_range(0xc0, 0xd6),
    regex_range(0xd8, 0xf6),
    regex_range(0xf8, 0xff),
    regex_range(0x0100, 0x024f),
    regex_range(0x0253, 0x0254),
    regex_range(0x0256, 0x0257),
    regex_range(0x0259),
    regex_range(0x025b),
    regex_range(0x0263),
    regex_range(0x0268),
    regex_range(0x026f),
    regex_range(0x0272),
    regex_range(0x0289),
    regex_range(0x028b),
    regex_range(0x02bb),
    regex_range(0x0300, 0x036f),
    regex_range(0x1e00, 0x1eff)
]
REGEXEN['latin_accents'] = re.compile(ur''.join(LATIN_ACCENTS))

REGEXEN['at_signs'] = re.compile(ur'[%s]' % ur'|'.join(list(u'@＠')))
REGEXEN['extract_mentions'] = re.compile(ur'(^|[^a-zA-Z0-9_])(%s)([a-zA-Z0-9_]{1,20})(?=(.|$))' % REGEXEN['at_signs'].pattern)
REGEXEN['extract_reply'] = re.compile(ur'^(?:[%s])*%s([a-zA-Z0-9_]{1,20})' % (REGEXEN['spaces'].pattern, REGEXEN['at_signs'].pattern))

# Characters considered valid in a hashtag but not at the beginning, where only a-z and 0-9 are valid.
HASHTAG_CHARACTERS = re.compile(ur'[a-z0-9_%s]' % REGEXEN['latin_accents'].pattern, re.IGNORECASE) 
REGEXEN['auto_link_hashtags'] = re.compile(ur'(^|[^0-9A-Z&\/]+)(#|＃)([0-9A-Z_]*[A-Z_]+%s*)' % HASHTAG_CHARACTERS.pattern, re.IGNORECASE)
REGEXEN['auto_link_usernames_or_lists'] = re.compile(ur'([^a-zA-Z0-9_]|^)([@＠]+)([a-zA-Z0-9_]{1,20})(\/[a-zA-Z][a-zA-Z0-9\u0080-\u00ff\-]{0,79})?')
REGEXEN['auto_link_emoticon'] = re.compile(ur'(8\-\#|8\-E|\+\-\(|\`\@|\`O|\&lt;\|:~\(|\}:o\{|:\-\[|\&gt;o\&lt;|X\-\/|\[:-\]\-I\-|\/\/\/\/Ö\\\\\\\\|\(\|:\|\/\)|∑:\*\)|\( \| \))')

# URL related hash regex collection
REGEXEN['valid_preceding_chars'] = re.compile(ur"(?:[^\/\"':!=]|^|\:)")
punct = re.escape(string.punctuation)
REGEXEN['valid_domain'] = re.compile(ur'(?:[^%s\s][\.-](?=[^%s\s])|[^%s\s]){1,}\.[a-z]{2,}(?::[0-9]+)?' % (punct, punct, punct), re.IGNORECASE)
REGEXEN['valid_url_path_chars'] = re.compile(ur'[\.\,]?[a-z0-9!\*\'\(\);:=\+\$\/%#\[\]\-_,~@\.]', re.IGNORECASE)
# Valid end-of-path chracters (so /foo. does not gobble the period).
#   1. Allow ) for Wikipedia URLs.
#   2. Allow =&# for empty URL parameters and other URL-join artifacts
REGEXEN['valid_url_path_ending_chars'] = re.compile(ur'[a-z0-9\)=#\/]', re.IGNORECASE)
REGEXEN['valid_url_query_chars'] = re.compile(ur'[a-z0-9!\*\'\(\);:&=\+\$\/%#\[\]\-_\.,~]', re.IGNORECASE)
REGEXEN['valid_url_query_ending_chars'] = re.compile(ur'[a-z0-9_&=#]', re.IGNORECASE)
REGEXEN['valid_url'] = re.compile(u'''
    (%s)
    (
        (https?:\/\/|www\.)
        (%s)
        (/%s*%s?)?
        (\?%s*%s)?
    )
    ''' % (
        REGEXEN['valid_preceding_chars'].pattern,
        REGEXEN['valid_domain'].pattern,
        REGEXEN['valid_url_path_chars'].pattern,
        REGEXEN['valid_url_path_ending_chars'].pattern,
        REGEXEN['valid_url_query_chars'].pattern,
        REGEXEN['valid_url_query_ending_chars'].pattern
    ),
re.IGNORECASE + re.X)
# groups:
# 1 - Preceding character
# 2 - URL
# 3 - Protocol or www.
# 4 - Domain and optional port number
# 5 - URL path
# 6 - Query string
