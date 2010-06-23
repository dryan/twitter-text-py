from twitter_text.autolink import Autolink
from twitter_text.extractor import Extractor
from twitter_text.highlighter import HitHighlighter
from twitter_text.unicode import force_unicode

class TwitterText(object):
    def __init__(self, text):
        self.text = force_unicode(text) # this will get modified by some functions
        self.original_text = self.text # this never changes; use it as a fallback or for comparison
        self.has_been_linked = False
        
    def __unicode__(self):
        return self.text
        
    def __repr__(self):
        return self.__unicode__()
    
    @property
    def autolink(self):
        return Autolink(self.text, parent = self)
        
    @property
    def extractor(self):
        return Extractor(self.text)
        
    @property
    def highlighter(self):
        return HitHighlighter(self.text, parent = self)