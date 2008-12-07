import os
import stat
from Logger import log


class FileMonitor(object):

    def __init__(self, db_wrapper, root_dir):
        self._db_wrapper = db_wrapper

        # initial walk
        self.add_dir(root_dir)
    
    def add_dir(self, root_dir):
        for (path, names) in self._walk_file_system(root_dir):
            for name in names:
                self._db_wrapper.add_file(path, name)

    def _walk_file_system(self, root):
        names = os.listdir(root)
        for name in names:
            try:
                st = os.lstat(os.path.join(root, name))
            except os.error:
                continue

            if stat.S_ISDIR(st.st_mode):
                for (newroot, children) in self._walk_file_system(os.path.join(root, name)):
                    yield newroot, children
        yield root, names

if __name__ == '__main__':
    from DBWrapper import DBWrapper
    db = DBWrapper()
    file_mon = FileMonitor(db, ".")
