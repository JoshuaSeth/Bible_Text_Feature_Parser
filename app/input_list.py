from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import save_load

class InputList(QGroupBox):
    def __init__(self, input_list=None, hooked_item=None):
        #Initialize element
        super(InputList, self).__init__()

        #Main layout
        self.top_layout = QVBoxLayout()
        self.setLayout(self.top_layout)
        self.top_layout.setAlignment(Qt.AlignTop)


        #An input list should always allow you to save or load it's contents as a preset
        box = QHBoxLayout()
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.OpenListPreset)
        box.addWidget(self.load_btn)
        self.save_btn = QPushButton("Save")
        box.addWidget(self.save_btn)
        self.top_layout.addLayout(box)

        #Input fields layout
        self.cur_layout = QGridLayout()
        self.top_layout.addLayout(self.cur_layout)
        self.cur_layout.setAlignment(Qt.AlignTop)

        self.hooked_item = hooked_item
        

        #Keep track of input lines
        self.edits = []

        self.entries = 0
        self.column_num = 0

        #If we get a predefined input_list
        if input_list != None:
            for item in input_list:
                self.AddLineEdit(string=item)
        #If we did not get a predefined list
        else:
            self.AddLineEdit()
    
    def OpenListPreset(self):
        input_list = save_load.OpenFile()
        self.SetList(input_list)

    def AddLineEdit(self, string=""):
        #Start a new column at 10 lines
        if self.entries == 10:
            self.column_num+=2
            self.entries = 0

        #Add an input field and save its state
        edit = QLineEdit()
        edit.setMinimumWidth(60)

        #Add initial vaule
        if string != "":
            edit.setText(string) 

        #On enter add another line
        edit.returnPressed.connect(self.AddLineEdit)

        #if this is connected to some list
        if self.hooked_item != None:
            #Then whenever the text of an input is changed change the contents of this hooked plugin
            edit.textChanged.connect(lambda state, x=self : self.hooked_item.OnListValChange(x))

        #Add the line to the layout
        self.cur_layout.addWidget(edit, self.entries, self.column_num)
        self.edits.append(edit)

        #Add a remove button
        btn = QPushButton("x")
        btn.setFixedWidth(30)
        self.cur_layout.addWidget(btn, self.entries, self.column_num+1)

        #Whenever text is set of some cell manually update the hooked list
        if self.hooked_item != None:
            self.hooked_item.OnListValChange(self)

        #Traack entries to place new line at
        self.entries+=1

    def SetList(self, input_list):
        #First clear
        self.Clear()

        #Then
        for item in input_list:
            self.AddLineEdit(string=item.replace("\n", ""))

    def Clear(self):
        #First remove all current LineEdits
        for i in reversed(range(self.cur_layout.count())): 
            self.cur_layout.itemAt(i).widget().deleteLater()

        #When clearing also clear edits otherwise we will have old iput fields
        self.edits = []

        #Start at the first entry
        self.entries=0
    
    def GetContents(self):
        # Fill a list with the text contents of the edit fields
        l = []
        for edit in self.edits:
            l.append(edit.text())
        return l
