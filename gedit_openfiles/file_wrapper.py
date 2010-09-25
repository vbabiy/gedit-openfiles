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

    def highlight_pattern(self, path):
        path = path.replace(self._root + "/", "") # Relative path
        log.debug("[FileWrapper] path = " + path)
        query_list = self._query_input.lower().split(" ")

        last_postion = 0
        for word in query_list:
            location = path.lower().find(word, last_postion)
            log.debug("[FileWrapper] Found Postion = " + str(location))
            if location > -1:
                last_postion = (location + len(word) + 40)
                a_path = list(path)
                a_path.insert(location, '<span weight="heavy" underline="single">')
                a_path.insert(location + len(word) + 1, "</span>")
                path = "".join(a_path)
        

        log.debug("[FileWrapper] Markup Path = " + path)
        return '%s' % path
