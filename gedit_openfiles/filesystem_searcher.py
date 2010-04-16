import urllib

from db_wrapper import DBWrapper
from filesystem_monitor import FilesystemMonitor
from file_wrapper import FileWrapper


class FilesystemSearcher(object):
    """
    Public API to be used by the UI to ask for files.

    TODO: Do we want to include hidden files should ask the file browserstop
    """

    def __init__(self, plugin, window):
        """
        Window handle setting up the database and file system monitor.
        """
        # defaults
        self._root = "."

        # Setup
        self._window = window
        self._plugin = plugin
        self._message_bus = self._window.get_message_bus()

        self._db = DBWrapper()
        self._monitor = None

        self._message_bus.connect('/plugins/filebrowser', 'root_changed', self.root_changed_callback)

    def root_changed_callback(self, bus, msg):
        previous_root = self._root
        self._root = msg.uri.replace("file://", "") # FIXME: HACK

        if not self._monitor:
            self._monitor = FilesystemMonitor(self)
        self._monitor.change_root(previous_root)
        

    @property
    def current_root(self):
        """
        Returns the current root location of the window.
        """
        if self.configuration.get_value("USE_FILEBROWSER"):
            return urllib.unquote(self._root)
        else:
            return urllib.unquote(self.configuration.get_value('STATIC_ROOT_PATH'))

    @property
    def configuration(self):
        return self._plugin._configuration

    def add_file(self, path, file_name):
        self._db.add_file(path, file_name)

    def remove_directory(self, path):
        self._db.remove_directory(path)

    def remove_file(self, path, name):
        self._db.remove_file(path, name)

    def search(self, input):
        query = self.current_root + "%" + input
        filewrappers = []
        for row in self._db.search(query):
            # FIXME: Set data in variables so you can tell what data is returned.
            filewrappers.append(FileWrapper(input, self.current_root, row[0], row[1]))
        return filewrappers
