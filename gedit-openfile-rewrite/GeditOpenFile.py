import gedit
from FileMonitor import FileMonitor
from DBWrapper import DBWrapper

menu_str="""
<ui>
    <menubar name="MenuBar">
        <menu name="FileMenu" action="File">
		    <placeholder name="FileOps_1">
			    <menuitem name="Open File" action="SnapOpenAction"/>
		    </placeholder>
	    </menu>
    </menubar>
</ui>
"""

class GeditOpenFile(gedit.Plugin):
    def __init__(self):
        # Create DB Wrapper and start the thread
        self._db_wrapper = DBWrapper()
        
        self._file_monitor = FileMonitor(self._db_wrapper)
        
    def activate(self, window):
        pass
    def deactivate(self, window):
        pass
    def update_ui(self, window):
        pass
    def _insert_menu(sefl):
        pass
