from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import input_list
import os
import weakref
import plugin_ui

class PluginsPane(QGroupBox):
    #Register instance
    _instances = set()

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def __init__(self):
        #Register this instance
        self._instances.add(weakref.ref(self))

        #Initialize element
        super(PluginsPane, self).__init__()

        #Give this widget a layout
        self.cur_layout = QVBoxLayout()
        self.setLayout(self.cur_layout)
        self.cur_layout.setAlignment(Qt.AlignTop)
        # self.cur_layout.setContentsMargins(2, 2, 2, 2)

        #The plugins title
        label = QLabel("Plugins")
        label.setFont(QFont('Arial', 28))
        qbox = QVBoxLayout()
        qbox.setAlignment(Qt.AlignCenter)
        qbox.addWidget(label)
        self.cur_layout.addLayout(qbox)

        #Make sure the column can't get to wide
        self.setMaximumWidth(600)
        #Add a box for the pluginsQVBoxLayout()
        self.plugins_uis = QVBoxLayout()
        self.cur_layout.addLayout(self.plugins_uis)
        self.plugins_uis.setAlignment(Qt.AlignTop)

        #Load all the plugin classes
        self.LoadAllPlugins()
    
    def Clear(self, layout):
        #Removes all plugin UIs
        #First remove all current LineEdits
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.Clear(item.layout())

        #When clearing also clear edits otherwise we will have old input fields
        self.active_plugins = []

    def LoadAllPlugins(self):
        #Load all the plugin classes
        import plugins.plugin_load as plugin_load
        self.plugins_library = plugin_load.LoadPlugins()

        self.active_plugins = []
        for plugin in self.plugins_library:
            #Instantiate all the classes
            self._InstantiatePlugin(plugin)

    def _InstantiatePlugin(self, plugin, preset=None):
        instantiate = plugin()

        #Fill the plugin with preset values
        if preset != None:
            instantiate.LoadPreset(preset)

        #If this is an enabled plugin render it
        if instantiate.enabled:
            #Keep track of them
            self.active_plugins.append(instantiate)

            #Give this instance to a pluginUI to create UI for it
            ui = plugin_ui.PluginUI(instantiate)
            self.plugins_uis.addWidget(ui)

            #Make the plugin aware of its ui
            instantiate.ui = ui
    
    def LoadPluginsFromWorkspace(self, workspace):
        #Empty the workspace when doing this
        self.Clear(self.plugins_uis)

        #Load the plugins by their names
        for plugin in workspace.__dict__["Plugins"]:
            self.OpenPluginByName(plugin[4], plugin)
    
    def OpenPluginByName(self, name, preset=None):
        print(self.plugins_library)
        plugin = self.FindPlugin(name)
        self._InstantiatePlugin(plugin, preset)


    def FindPlugin(self, name):
        for plugin in self.plugins_library:
            if str(plugin) == "<class 'plugins.{}'>".format(name):
                return plugin
        return None






