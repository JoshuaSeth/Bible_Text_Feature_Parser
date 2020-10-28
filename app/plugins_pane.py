from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from input_list import InputList
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

        #Load all the plugin classes
        import plugins.plugin_load as plugin_load
        plugins = plugin_load.LoadPlugins()

        self.active_plugins = []
        for plugin in plugins:
            #Instantiate all the classes
            instantiate = plugin()

            #Keep track of them
            self.active_plugins.append(instantiate)

            #Give this instance to a pluginUI to create UI for it
            self.cur_layout.addWidget(PluginUI(instantiate))


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
            #If the setting type is boolean make a checkbox
            if type(setting.value) is bool:
                label = QLabel(name)
                cb = QCheckBox()
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
                if len(setting.value)==0:
                    input_list = InputList()
                else:
                    input_list = InputList(setting.value)
                layout.addWidget(input_list)
            index+=1






