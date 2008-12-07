"""
File Monitor Contains
- FileMonitor Class
-- Keeps track of files with in a give tree

- WalkDirectoryThread
-- Thread to walk through the tree and store the file paths to a DBWrapper
"""
import os
import stat
from Logger import log
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent
from threading import Thread

EVENT_MASK = EventsCodes.IN_DELETE | EventsCodes.IN_CREATE | EventsCodes.IN_MOVED_TO | EventsCodes.IN_MOVED_FROM # watched events

class FileMonitor(object):
    """
    FileMonitor Class keeps track of all files down a tree starting at the root
    """

    def __init__(self, db_wrapper, root):
        self._db_wrapper = db_wrapper
        self._root = root

        # Add a watch to the root of the dir
        self._watch_manager = WatchManager()
        self._notifier = ThreadedNotifier(self._watch_manager, FileProcessEvent(self._db_wrapper)).start()
        self._watch_manager.add_watch(self._root, EVENT_MASK, rec=True, auto_add=True)

        # initial walk
        self.add_dir()

    def add_dir(self):
        """
        Starts a WalkDirectoryThread to add the directory
        """
        WalkDirectoryThread(self._db_wrapper, self._root)

class WalkDirectoryThread(Thread):
    """
    Thread that will take a DBWrapper and a root directory and add ever file
    to the database.
    """

    def __init__(self, db_wrapper, root):
        Thread.__init__(self)
        self._db_wrapper = db_wrapper
        self._root = root
        self.start()

    def run(self):
        """
        Runs the Thread
        """
        for (path, names) in self._walk_file_system(self._root):
            for name in names:
                self._db_wrapper.add_file(path, name)

    def _walk_file_system(self, root):
        """
        From a give root of a tree this method will walk through ever branch
        and return a generator.
        """
        names = os.listdir(root)
        for name in names:
            try:
                file_stat = os.lstat(os.path.join(root, name))
            except os.error:
                continue

            if stat.S_ISDIR(file_stat.st_mode):
                for (newroot, children) in self._walk_file_system(
                    os.path.join(root, name)):
                    yield newroot, children
        yield root, names


class FileProcessEvent(ProcessEvent):
    def __init__(self, db_wrapper):
        self._db_wrapper = db_wrapper

    def process_IN_CREATE(self, event):
        path = os.path.join(event.path, event.name)
        log.info("[FileProcessEvent] CREATED: " + path)
        self._db_wrapper.add_file(event.path, event.name)

    def process_IN_DELETE(self, event):
        path = os.path.join(event.path, event.name)
        log.info("[FileProcessEvent] DELETED: " + path)
        self._db_wrapper.remove_file(event.path, event.name)

    def process_IN_MOVED_FROM(self, event):
        path = os.path.join(event.path, event.name)
        log.info("[FileProcessEvent] MOVED_FROM: " + path)
        self.process_IN_DELETE(event)

    def process_IN_MOVED_TO(self, event):
        path = os.path.join(event.path, event.name)
        log.info("[FileProcessEvent] MOVED_TO: " + path)
        self.process_IN_CREATE(event)


if __name__ == '__main__':
    from DBWrapper import DBWrapper
    db = DBWrapper()
    file_mon = FileMonitor(db, ".")
