"""
File Monitor Contains
- FileMonitor Class
-- Keeps track of files with in a give tree

- WalkDirectoryThread
-- Thread to walk through the tree and store the file paths to a DBWrapper
"""
import os
import stat


class FileMonitor(object):
    """
    FileMonitor Class keeps track of all files down a tree starting at the root
    """

    def __init__(self, db_wrapper, root):
        self._db_wrapper = db_wrapper
        self._root = root

        # initial walk
        self.add_dir()

    def add_dir(self):
        """
        Starts a WalkDirectoryThread to add the directory
        """
        WalkDirectoryThread(self._db_wrapper, self._root)

    def remove_dir(self):
        """
        Remove a directory from the watch
        """
        pass

from threading import Thread


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


if __name__ == '__main__':
    from DBWrapper import DBWrapper
    db = DBWrapper()
    file_mon = FileMonitor(db, ".")
