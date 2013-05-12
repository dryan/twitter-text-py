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
LATIN_ACCENTS = ''.join(LATIN_ACCENTS)

RTL_CHARACTERS = ''.join([
    regex_range(0x0600,0x06FF),
    regex_range(0x0750,0x077F),
    regex_range(0x0590,0x05FF),
    regex_range(0xFE70,0xFEFF)
])

NON_LATIN_HASHTAG_CHARS = ''.join([
    # Cyrillic (Russian, Ukrainian, etc.)
    regex_range(0x0400, 0x04ff), # Cyrillic
    regex_range(0x0500, 0x0527), # Cyrillic Supplement
    regex_range(0x2de0, 0x2dff), # Cyrillic Extended A
    regex_range(0xa640, 0xa69f), # Cyrillic Extended B
    regex_range(0x0591, 0x05bf), # Hebrew
    regex_range(0x05c1, 0x05c2),
    regex_range(0x05c4, 0x05c5),
    regex_range(0x05c7),
    regex_range(0x05d0, 0x05ea),
    regex_range(0x05f0, 0x05f4),
    regex_range(0xfb12, 0xfb28), # Hebrew Presentation Forms
    regex_range(0xfb2a, 0xfb36),
    regex_range(0xfb38, 0xfb3c),
    regex_range(0xfb3e),
    regex_range(0xfb40, 0xfb41),
    regex_range(0xfb43, 0xfb44),
    regex_range(0xfb46, 0xfb4f),
    regex_range(0x0610, 0x061a), # Arabic
    regex_range(0x0620, 0x065f),
    regex_range(0x066e, 0x06d3),
    regex_range(0x06d5, 0x06dc),
    regex_range(0x06de, 0x06e8),
    regex_range(0x06ea, 0x06ef),
    regex_range(0x06fa, 0x06fc),
    regex_range(0x06ff),
    regex_range(0x0750, 0x077f), # Arabic Supplement
    regex_range(0x08a0),         # Arabic Extended A
    regex_range(0x08a2, 0x08ac),
    regex_range(0x08e4, 0x08fe),
    regex_range(0xfb50, 0xfbb1), # Arabic Pres. Forms A
    regex_range(0xfbd3, 0xfd3d),
    regex_range(0xfd50, 0xfd8f),
    regex_range(0xfd92, 0xfdc7),
    regex_range(0xfdf0, 0xfdfb),
    regex_range(0xfe70, 0xfe74), # Arabic Pres. Forms B
    regex_range(0xfe76, 0xfefc),
    regex_range(0x200c, 0x200c), # Zero-Width Non-Joiner
    regex_range(0x0e01, 0x0e3a), # Thai
    regex_range(0x0e40, 0x0e4e), # Hangul (Korean)
    regex_range(0x1100, 0x11ff), # Hangul Jamo
    regex_range(0x3130, 0x3185), # Hangul Compatibility Jamo
    regex_range(0xA960, 0xA97F), # Hangul Jamo Extended-A
    regex_range(0xAC00, 0xD7AF), # Hangul Syllables
    regex_range(0xD7B0, 0xD7FF), # Hangul Jamo Extended-B
    regex_range(0xFFA1, 0xFFDC)  # Half-width Hangul
])

CJ_HASHTAG_CHARACTERS = ''.join([
    regex_range(0x30A1, 0x30FA), regex_range(0x30FC, 0x30FE), # Katakana (full-width)
    regex_range(0xFF66, 0xFF9F), # Katakana (half-width)
    regex_range(0xFF10, 0xFF19), regex_range(0xFF21, 0xFF3A), regex_range(0xFF41, 0xFF5A), # Latin (full-width)
    regex_range(0x3041, 0x3096), regex_range(0x3099, 0x309E), # Hiragana
    regex_range(0x3400, 0x4DBF), # Kanji (CJK Extension A)
    regex_range(0x4E00, 0x9FFF), # Kanji (Unified)
])
try:
    CJ_HASHTAG_CHARACTERS   =   ''.join([
        CJ_HASHTAG_CHARACTERS,
        regex_range(0x20000, 0x2A6DF), # Kanji (CJK Extension B)
        regex_range(0x2A700, 0x2B73F), # Kanji (CJK Extension C)
        regex_range(0x2B740, 0x2B81F), # Kanji (CJK Extension D)
        regex_range(0x2F800, 0x2FA1F), regex_range(0x3003), regex_range(0x3005), regex_range(0x303B) # Kanji (CJK supplement)
    ])
except ValueError:
    # this is a narrow python build so we can't process the higher characters
    pass

PUNCTUATION_CHARS = ur'!"#$%&\'()*+,-./:;<=>?@\[\]^_\`{|}~'
SPACE_CHARS = ur" \t\n\x0B\f\r"
CTRL_CHARS = ur"\x00-\x1F\x7F"

HASHTAG_ALPHA = ur'[a-z_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)
HASHTAG_ALPHANUMERIC = ur'[a-z0-9_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)
HASHTAG_BOUNDARY = ur'\A|\z|[^&a-z0-9_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)

HASHTAG = re.compile(ur'(%s)(#|＃)(%s*%s%s*)' % (HASHTAG_BOUNDARY, HASHTAG_ALPHANUMERIC, HASHTAG_ALPHA, HASHTAG_ALPHANUMERIC), re.IGNORECASE)

REGEXEN['valid_hashtag'] = HASHTAG
REGEXEN['end_hashtag_match'] = ur'\A(?:[#＃]|:\/\/)'

REGEXEN['valid_mention_preceding_chars'] = re.compile(r'(?:[^a-zA-Z0-9_!#\$%&*@＠]|^|RT:?)')
REGEXEN['at_signs'] = re.compile(ur'[@＠]')
REGEXEN['valid_mention_or_list'] = re.compile(
    REGEXEN['valid_mention_preceding_chars'].pattern.decode('utf-8') +  # preceding character
    REGEXEN['at_signs'].pattern +                                       # at mark
    ur'([a-zA-Z0-9_]{1,20})' +                                          # screen name
    ur'(\/[a-zA-Z][a-zA-Z0-9_\-]{0,24})?'                               # list (optional)
)

REGEXEN['valid_reply'] = re.compile(ur'^(?:%s)*%s([a-zA-Z0-9_]{1,20})' % (REGEXEN['spaces'].pattern, REGEXEN['at_signs'].pattern))
REGEXEN['end_mention_match'] = re.compile(ur'\A(?:%s|%s|:\/\/)' % (REGEXEN['at_signs'].pattern, REGEXEN['latin_accents'].pattern))

REGEXEN['extract_mentions'] = re.compile(ur'(^|[^a-zA-Z0-9_])(%s)([a-zA-Z0-9_]{1,20})(?=(.|$))' % REGEXEN['at_signs'].pattern)
REGEXEN['extract_reply'] = re.compile(ur'^(?:[%s])*%s([a-zA-Z0-9_]{1,20})' % (REGEXEN['spaces'].pattern, REGEXEN['at_signs'].pattern))

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
