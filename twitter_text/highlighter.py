# encoding=utf-8

import re
from HTMLParser import HTMLParser

from twitter_text.regex import UNICODE_SPACES
from twitter_text.unicode import force_unicode

DEFAULT_HIGHLIGHT_TAG = 'em'

# from http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class HitHighlighter(object):
    def __init__(self, text, **kwargs):
        self.text = force_unicode(text)
        self.parent = kwargs.get('parent', False)

    def hit_highlight(self, hits = [], **kwargs):
        if not hits:
            return self.text

        tag_name = kwargs.get('tag', DEFAULT_HIGHLIGHT_TAG)
        tags = [u'<%s>' % tag_name, u'</%s>' % tag_name]

        text = self.text
        chunks = re.split(r'[<>]', text)
        text_chunks = []
        for index, chunk in enumerate(chunks):
            if not index % 2:
                text_chunks.append(chunk)
        for hit in sorted(hits, key = lambda chunk: chunk[1], reverse = True):
            hit_start, hit_end = hit
            placed = 0
            for index, chunk in enumerate(chunks):
                if placed == 2:
                    continue
                if index % 2:
                    # we're inside a <tag>
                    continue
                chunk_start = len(u''.join(text_chunks[0:index / 2]))
                chunk_end = chunk_start + len(chunk)
                if hit_start >= chunk_start and hit_start < chunk_end:
                    chunk = chunk[:hit_start - chunk_start] + tags[0] + chunk[hit_start - chunk_start:]
                    if hit_end < chunk_end:
                        hit_end += len(tags[0])
                        chunk_end += len(tags[0])
                    placed = 1
                if hit_end > chunk_start and hit_end < chunk_end:
                    chunk = chunk[:hit_end - chunk_start] + tags[1] + chunk[hit_end - chunk_start:]
                    placed = 2
                chunks[index] = chunk
            if placed == 1:
                chunks[-1] = chunks[-1] + tags[1]
        result = []
        for index, chunk in enumerate(chunks):
            if index % 2:
                # we're inside a <tag>
                result.append(u'<%s>' % chunk)
            else:
                result.append(chunk)
        self.text = u''.join(result)
        return self.text