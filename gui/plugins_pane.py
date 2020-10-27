from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from input_list import InputList
from check_combo_box import CheckableComboBox
import os


class PluginsPane(QGroupBox):
    def __init__(self):
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

        import plugins.plugin_load as plugin_load
        plugins = plugin_load.LoadPlugins()

        for plugin in plugins:
            self.cur_layout.addWidget(PluginUI(plugin()))


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

            if type(setting.value) is str:
                label = QLabel(name)
                inp = QLineEdit()
                label.setToolTip(setting.tooltip)
                grid.addWidget(label, index, 0)
                grid.addWidget(inp, index, 1)
            
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






