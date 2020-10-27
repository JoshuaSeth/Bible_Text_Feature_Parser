from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class InputList(QGroupBox):
    def __init__(self, input_list=None):
        #Initialize element
        super(InputList, self).__init__()

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
            #Then build form the items in these list
            self.entries = 1
            for item in input_list:
                self.AddLineEdit()
                self.entries+=1
        #If we did not get a predefined list
        else:
            self.AddLineEdit()

    def AddLineEdit(self):
        
        
        #Start a new column at 10 lines
        if self.entries == 10:
            self.column_num+=2
            self.entries = 0

        #Add an input field and save its state
        edit = QLineEdit()
        edit.returnPressed.connect(self.AddLineEdit)
        self.cur_layout.addWidget(edit, self.entries, self.column_num)
        self.edits.append(edit)

        #Add a remove button
        btn = QPushButton()
        self.cur_layout.addWidget(btn, self.entries, self.column_num+1)

        #Traack entries to place new line at
        self.entries+=1






