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

        #Check if longlist is set
        self.long_list = False
        
        #Keep track of the original supplied input list
        self.start_list = input_list

        #An input list should always allow you to save or load it's contents as a preset
        box = QHBoxLayout()
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.OpenListPreset)
        box.addWidget(self.load_btn)
        self.save_btn = QPushButton("Save")
        box.addWidget(self.save_btn)
        self.save_btn.clicked.connect(lambda x: save_load.SaveList(self.GetContents()))
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
        edit = QLineEdit("",self)
        edit.setMinimumWidth(60)

        #Put cursor in here
        edit.setFocusPolicy(Qt.StrongFocus)
        edit.setFocus()

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
        
        #If we have line edits we are not a long list
        self.long_list=False

        #Traack entries to place new line at
        self.entries+=1

    def SetList(self, input_list):
        #First clear
        self.Clear()

        #If it is not a too long list
        if len(input_list) < 41:
            #Then
            for item in input_list:
                self.AddLineEdit(string=str(item).replace("\n", ""))
        #Else if it is to long render the list as longlistinfo
        else:
            self.SetLongListMode(input_list)
        
        #Notify the connected setting that the list value has changed
        if self.hooked_item != None:
            self.hooked_item.OnListValChange(self)

    def Clear(self):
        #First remove all current LineEdits
        for i in reversed(range(self.cur_layout.count())): 
            self.cur_layout.itemAt(i).widget().deleteLater()

        #When clearing also clear edits otherwise we will have old iput fields
        self.edits = []

        #Start at the first entry
        self.entries=0
    
    def GetContents(self):
        #If we are in line edit mode
        if self.long_list == False:
            # Fill a list with the text contents of the edit fields
            l = []
            for edit in self.edits:
                l.append(edit.text())
            return l
        #If we are an uneditable long list
        else:
            #return the original supplied list
            return self.start_list

    def SetLongListMode(self, input_list=None):
        #Only displays information about the list if the list has to many items

        #Display entries
        label = QLabel("{} terms".format(str(len(input_list))))
        self.top_layout.addWidget(label)

        #Display first and last
        #Make a string with the first and last word
        first_word = input_list[0]
        second_word = input_list[1]
        third_word = input_list[2]
        last_word  = input_list[len(input_list)-1]
        sec_last_word  = input_list[len(input_list)-2]
        third_last_word  = input_list[len(input_list)-3]
        #Concatenate to something nice
        total = "Terms:  {}, {}, {} ... {}, {}, {}".format(first_word, second_word, third_word, third_last_word, sec_last_word, last_word)
        #Display information about first and last words
        label2 = QLabel(total)
        self.top_layout.addWidget(label2)

        #We are now in longlist mode
        self.long_list=True

        self.start_list = input_list
