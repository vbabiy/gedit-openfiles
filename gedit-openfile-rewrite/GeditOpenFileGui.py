import gtk
import os

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


class GeditOpenGui(object):

    def __init__(self, plugin, window):
        self._window = window

        # Get Builder and get xml file
        self._builder = gtk.Builder()
        self._builder.add_from_file(os.path.join(os.path.dirname(__file__),
             "gui", "geditopenfiles_gtk.xml"))

        #setup window
        self._plugin_window = self._builder.get_object("gedit_openfiles_window")
        self._plugin_window.connect("key-release-event", self._on_key_release)
        self._plugin_window.set_transient_for(self._window)

        #setup buttons
        self._builder.get_object("open_button").connect("clicked",
            self.open_selected_item)
        self._builder.get_object("cancel_button").connect("clicked",
            lambda a: self._plugin_window.hide())

        # Setup entry field
        self._file_query = self._builder.get_object("file_query")
        self._file_query.connect("key-release-event", self._on_query_entry)

        # Get File TreeView
        self._file_list = self._builder.get_object("file_list")

        # Connect Action on TreeView
        self._file_list.connect("select-cursor-row", self._on_select_from_list)
        self._file_list.connect("button_press_event", self._on_list_mouse)

        # Setup File TreeView
        self._liststore = gtk.ListStore(str, str)
        self._file_list.set_model(self._liststore)

        # Path Column
        column1 = gtk.TreeViewColumn("Path", gtk.CellRendererText(), markup=0)
        column1.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self._file_list.append_column(column1)
        self._file_list.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        # Add Animation icon for building data
        building_data_spinner = self._builder.get_object('spinner')
        building_data_spinner.set_from_animation(gtk.gdk.PixbufAnimation(
            os.path.join(os.path.dirname(__file__), "gui", "progress.gif")))
        self._building_data_spinner_box = self._builder.get_object('spinner_box')

    def _insert_menu(self):
        pass

    def _on_key_release(self, event):
        pass

    def _on_query_entry(self, event):
        pass

    def _on_select_from_list(self, event):
        pass

    def _on_list_mouse(self, event):
        pass

    def open_selected_item(self):
        pass
