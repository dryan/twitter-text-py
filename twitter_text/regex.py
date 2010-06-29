#  encoding=utf-8

# A collection of regular expressions for parsing Tweet text. The regular expression
# list is frozen at load time to ensure immutability. These reular expressions are
# used throughout the Twitter classes. Special care has been taken to make
# sure these reular expressions work with Tweets in all languages.
import re, string

REGEXEN = {} # :nodoc:

# Space is more than %20, U+3000 for example is the full-width space used with Kanji. Provide a short-hand
# to access both the list of characters and a pattern suitible for use with String#split
#  Taken from: ActiveSupport::Multibyte::Handlers::UTF8Handler::UNICODE_WHITESPACE
UNICODE_SPACES = []
for space in [9, 10, 11, 12, 13, 32, 133, 160, 5760, 6158, 8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199, 8200, 8201, 8202, 8232, 8233, 8239, 8287, 12288]:
    UNICODE_SPACES.append(hex(space))
REGEXEN['spaces'] = re.compile(ur'|'.join(UNICODE_SPACES))

REGEXEN['at_signs'] = re.compile(ur'[%s]' % ur'|'.join(list(u'@＠')))
REGEXEN['extract_mentions'] = re.compile(ur'(^|[^a-zA-Z0-9_])(%s)([a-zA-Z0-9_]{1,20})(?=(.|$))' % REGEXEN['at_signs'].pattern)
REGEXEN['extract_reply'] = re.compile(ur'^(?:[%s])*%s([a-zA-Z0-9_]{1,20})' % (REGEXEN['spaces'].pattern, REGEXEN['at_signs'].pattern))

REGEXEN['list_name'] = re.compile(ur'^[a-zA-Z\u0080-\u00ff].{0,79}$')

# Latin accented characters (subtracted 0xD7 from the range, it's a confusable multiplication sign. Looks like "x")
LATIN_ACCENTS = []
for accent in [192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 248, 249, 250, 251, 252, 253, 254, 255]:
    LATIN_ACCENTS.append(hex(accent))
REGEXEN['latin_accents'] = re.compile(ur''.join(LATIN_ACCENTS))

# Characters considered valid in a hashtag but not at the beginning, where only a-z and 0-9 are valid.
HASHTAG_CHARACTERS = re.compile(ur'[a-z0-9_%s]' % REGEXEN['latin_accents'].pattern, re.IGNORECASE) 
REGEXEN['auto_link_hashtags'] = re.compile(ur'(^|[^0-9A-Z&\/]+)(#|＃)([0-9A-Z_]*[A-Z_]+%s*)' % HASHTAG_CHARACTERS.pattern, re.IGNORECASE)
REGEXEN['auto_link_usernames_or_lists'] = re.compile(ur'([^a-zA-Z0-9_]|^)([@＠]+)([a-zA-Z0-9_]{1,20})(\/[a-zA-Z][a-zA-Z0-9\u0080-\u00ff\-]{0,79})?')
REGEXEN['auto_link_emoticon'] = re.compile(ur'(8\-\#|8\-E|\+\-\(|\`\@|\`O|\&lt;\|:~\(|\}:o\{|:\-\[|\&gt;o\&lt;|X\-\/|\[:-\]\-I\-|\/\/\/\/Ö\\\\\\\\|\(\|:\|\/\)|∑:\*\)|\( \| \))')

# URL related hash regex collection
REGEXEN['valid_preceding_chars'] = re.compile(ur"(?:[^\/\"':!=]|^|\:)")
punct = re.escape(string.punctuation)
REGEXEN['valid_domain'] = re.compile(ur'(?:[^%s\s][\.-](?=[^%s\s])|[^%s\s]){1,}\.[a-z]{2,}(?::[0-9]+)?' % (punct, punct, punct), re.IGNORECASE)
REGEXEN['valid_url_path_chars'] = re.compile(ur'[\.\,]?[a-z0-9!\*\'\(\);:=\+\$\/%#\[\]\-_,~@]', re.IGNORECASE)
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