from autolink import Autolink
from extractor import Extractor

class TwitterText(object):
    def __init__(self, text):
        self.text = unicode(text) # this will get modified by some functions
        self.original_text = self.text # this never changes; use it as a fallback or for comparison
        self.autolink = Autolink(self.text, parent = self)
        self.extractor = Extractor(self.text)
        
    def __unicode__(self):
        return self.text
        
    def __repr__(self):
        return self.__unicode__()