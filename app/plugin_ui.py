from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import input_list
from check_combo_box import CheckableComboBox
from pic_button import PicButton
import plugins_pane

#Display a plugin
class PluginUI(QGroupBox):
    def __init__(self, plugin=None):
        super(PluginUI, self).__init__()

        #Give this widget a layout
        layout = QVBoxLayout()

        #Track the actual plugin connected
        self.plugin = plugin

        #Make layout start at top instead of middle
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        #Give the plugin a title
        label = QLabel(plugin.name)
        label.setFont(QFont('Arial', 24))

        #Give it a close button
        pixmap = QPixmap("/Users/sethvanderbijl/Coding Projects/Bible_features/app/close.png")
        close = PicButton(pixmap)
        close.setMaximumWidth(20)
        close.setMaximumHeight(20)
        close.clicked.connect(self.ClosePlugin)

        #Give it a save button
        save = QPushButton("Save Preset")
        save.setMaximumWidth(100)

        #Give the top a container
        top = QHBoxLayout()
        layout.addLayout(top)
        top.addWidget(label)
        top.addWidget(save)
        top.addWidget(close)

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
                self.cbb = cbb
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

    def ClosePlugin(self):
        for pp in plugins_pane.PluginsPane.getinstances():
            pp.ClosePlugin(self)