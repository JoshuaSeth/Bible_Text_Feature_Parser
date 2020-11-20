from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import input_list
from check_combo_box import CheckableComboBox
import os
import weakref


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
            ui = PluginUI(instantiate)
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





#Display a plugin
class PluginUI(QGroupBox):
    def __init__(self, plugin=None):
        super(PluginUI, self).__init__()

        #Give this widget a layout
        layout = QVBoxLayout()

        #Make layout start at top instead of middle
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        #Give the plugin a title
        label = QLabel(plugin.name)
        label.setFont(QFont('Arial', 20))
        layout.addWidget(label)

        #Put the settings in a grid
        grid = QGridLayout()
        layout.addLayout(grid)

        index = 0
        for name, setting in plugin.settings.items():
            #If it is an int make a spinbox
            if type(setting.value) is int:
                label = QLabel(name)
                cb = QSpinBox()
                cb.setValue(setting.value)
                print("creating spinbox", setting, setting.value)
                setting.ui = cb
                cb.valueChanged.connect(setting.OnIntChanged)
                label.setToolTip(setting.tooltip)
                grid.addWidget(label, index, 0)
                grid.addWidget(cb, index, 1)

            #If the setting type is boolean make a checkbox
            if type(setting.value) is bool:
                label = QLabel(name)
                cb = QCheckBox()
                cb.setChecked(setting.value)
                cb.stateChanged.connect(setting.Tick)
                label.setToolTip(setting.tooltip)
                grid.addWidget(label, index, 0)
                grid.addWidget(cb, index, 1)

            #If it is a string make an input field
            if type(setting.value) is str:
                label = QLabel(name)
                inp = QLineEdit()
                label.setToolTip(setting.tooltip)
                grid.addWidget(label, index, 0)
                grid.addWidget(inp, index, 1)
            
            #If it is a set make a dropdown
            if type(setting.value) is set:
                label = QLabel(name)
                cbb = CheckableComboBox(setting.value)
                label.setToolTip(setting.tooltip)
                grid.addWidget(label, index, 0)
                grid.addWidget(cbb, index, 1)

            #If the setting type is list make na input list
            if type(setting.value) is list:
                space = QLabel("")
                label = QLabel(name)
                label.setToolTip(setting.tooltip)
                layout.addWidget(space)
                layout.addWidget(label)
                label.setFont(QFont('Arial', 16))
                #By hooking the setting to the input list the settings contents are updated whenever one of the input fields updates
                if len(setting.value)==0:
                    i_list = input_list.InputList(hooked_item=setting)
                else:
                    i_list = input_list.InputList(setting.value, hooked_item=setting)
                layout.addWidget(i_list)

            index+=1






