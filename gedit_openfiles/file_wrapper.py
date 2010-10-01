import urllib
import os
import gio

from logger import log

ext_file_language = {}

class FileWrapper(object):
    """
    A file wrapper.
    """
    def __init__(self, query_input, root, name, path, open_count=0):
        self._path = path
        self._name = name
        self._query_input = query_input
        self._root = root
        self._open_count = open_count

    @property
    def path(self):
        return self._path

    @property
    def uri(self):
        uri = "file://" + urllib.quote(self._path)
        return uri

    @property
    def display_path(self):
        return self.highlight_pattern(self._path)
    
    @property
    def type(self):
        content_type = gio.File(self._path).query_info('standard::*').get_content_type()
        return gio.content_type_get_description(content_type).title().split(" ")[0]
    
    @property
    def icon(self):
        return gio.File(self._path).query_info('standard::icon').get_icon()
    
    @property
    def open_count(self):
        return self._open_count
    
    def _highlight_tokens(self, tokens, string):
        token = tokens.pop(0)
        start, middle, end = string.partition(token)
        if end and tokens:
            end = self._highlight_tokens(tokens, end)
#        return '%s<span weight="heavy" underline="single">%s</span>%s' % (start, middle, end)
        return '%s<span weight="heavy">%s</span>%s' % (start, middle, end)

    def highlight_pattern(self, path):
        result = self._highlight_tokens(self._query_input.split(), 
          path.replace(self._root + "/", ""))
        log.debug("[FileWrapper] Markup Path = " + result)
        return result
