# -*- coding: utf-8 -*-
from gi.repository import GObject, Gedit
from completion import PythonProvider


class PythonKitPlugin(GObject.Object, Gedit.WindowActivatable):

    __gtype_name__ = "PythonKitPlugin"

    window = GObject.property(type=Gedit.Window)

    WINDOW_DATA_KEY = "PythonKitData"

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._provider = PythonProvider(self)
        for view in self.window.get_views():
            self.add_provider(view)
        self._tab_added_id = self.window.connect('tab-added',
            self.on_tab_added)
        self._tab_removed_id = self.window.connect('tab-removed',
            self.on_tab_removed)
        self.window.set_data(self.WINDOW_DATA_KEY, self.window)

    def do_deactivate(self):
        for view in self.window.get_views():
            self.remove_provider(view)
        self.window.disconnect(self._tab_added_id)
        self.window.disconnect(self._tab_removed_id)
        self.window.set_data(self.WINDOW_DATA_KEY, None)

    def do_update_state(self):
        pass

    def add_provider(self, view):
        """ Add provider to the new view. """
        view.get_completion().add_provider(self._provider)

    def remove_provider(self, view):
        """ Remove provider from the view. """
        view.get_completion().remove_provider(self._provider)

    def on_tab_added(self, window, tab):
        self.add_provider(tab.get_view())

    def on_tab_removed(self, window, tab):
        self.remove_provider(tab.get_view())
