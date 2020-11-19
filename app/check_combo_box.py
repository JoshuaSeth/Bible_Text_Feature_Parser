from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DropDownList(QGroupBox):
    def __init__(self, input_list=None):
        #Initialize element
        super(DropDownList, self).__init__()

        #Give this widget a layout
        self.cur_layout = QGridLayout()
        self.setLayout(self.cur_layout)
        self.cur_layout.setAlignment(Qt.AlignTop)

        #Keep track of input lines
        self.edits = []

        self.entries = 0
        self.column_num = 0

        #If we get a predefined input_list
        if input_list != None:
            for item in input_list:
                self.AddLineEdit(string=item)
                self.entries+=1
        #If we did not get a predefined list
        else:
            self.AddLineEdit()

    def AddLineEdit(self, string=""):
        #Start a new column at 10 lines
        if self.entries == 10:
            self.column_num+=2
            self.entries = 0

        #Add an input field and save its state
        edit = QLineEdit()

        #Add initial vaule
        if string != "":
            edit.setText(string)

        #On enter add another line
        edit.returnPressed.connect(self.AddLineEdit)

        #Add the line to the layout
        self.cur_layout.addWidget(edit, self.entries, self.column_num)
        self.edits.append(edit)

        #Add a remove button
        btn = QPushButton()
        self.cur_layout.addWidget(btn, self.entries, self.column_num+1)

        #Traack entries to place new line at
        self.entries+=1

class CheckableComboBox(QComboBox):
    def __init__(self, options):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))

        for option in options:
            self.addItem(option)


    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
    
    def GetContent(self):
        content = []
        model = self.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.checkState() == Qt.Checked:
                content.append(item.text())
        return content
