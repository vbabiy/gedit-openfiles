from threading import Thread
from Queue import Queue
import sqlite3
from Logger import log
import os


class DBWrapper(Thread):
    """
    Class to wrap the python sqlite3 module to support mulit threading
    """

    def __init__(self):
        # Create Database and a queue
        Thread.__init__(self)
        self._queue = Queue()
        self.start()

    def run(self):
        self._create_db()
        while True:
            if not self._queue.empty():
                sql, params, result = self._queue.get()
                cursor = self._db.cursor()
                if params:
                    cursor.execute(sql % params)
                    if result:
                        result.put(cursor.fetchall())
                else:
                    cursor.execute(sql)
                    if result:
                        result.put(cursor.fetchall())
                self._db.commit()

    def execute(self, sql, params=None, result=None):
        self._queue.put((sql, params, result))

    def select(self, sql, params=None):
        result = Queue()
        if params:
            self.execute(sql % params, result)
        else:
            self.execute(sql, result=result)

        while True:
            if not result.empty():
                return result.get()

        return cursor.fetchall()

    def close(self):
        self._queue.put("__CLOSE__")

    def _create_db(self):
        self._db = sqlite3.connect(":memory:")
        self.execute("CREATE TABLE files ( id AUTO_INCREMENT PRIMARY KEY, " +
            "path VARCHAR(255), name VARCHAR(255), " +
            "open_count INTEGER DEFAULT 0)")

    def add_file(self, path, name):
        log.debug("[DBWrapper] Adding File: " + os.path.join(path, name))
        self.execute("INSERT INTO files (name, path) VALUES ('%s', '%s')",
            (name, path))

    def remove_file(self, path, name):
        path = os.path.join(path, name)
        log.debug("[DBWrapper] Removing File: " + path)
        self.execute("DELETE FROM files where path = '%s'", (path, ))

if __name__ == '__main__':
    db = DBWrapper()
    db.execute("INSERT INTO files (path, name) VALUES ('%s', '%s')",
         ("vbabiy", "/home/vbabiy"))
    print (db.select("SELECT * FROM files"))
