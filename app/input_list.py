from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import save_load
from pic_button import PicButton

class InputList(QGroupBox):
    def __init__(self, input_list=None, hooked_item=None, has_columns=True, allow_summary=False):
        #Initialize element
        super(InputList, self).__init__()

        #Main layout
        self.top_layout = QVBoxLayout()
        self.setLayout(self.top_layout)
        self.top_layout.setAlignment(Qt.AlignTop)

        #Track some bools
        self.has_columns = has_columns
        self.allow_summary = allow_summary

        #Check if longlist is set
        self.long_list = False
        
        #Keep track of the original supplied input list
        self.start_list = input_list

        #An input list should always allow you to save or load it's contents as a preset
        box = QHBoxLayout()
        self.top_layout.addLayout(box)

        #Create a loadbutton
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.OpenListPreset)
        box.addWidget(self.load_btn)
        
        #Create a save button
        self.save_btn = QPushButton("Save")
        box.addWidget(self.save_btn)
        self.save_btn.clicked.connect(lambda x: save_load.SaveFile(self.GetContents()))

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
            #If this list has more than 20 items and we are allowed to summarize it
            if self.allow_summary and len(input_list) > 20:
                self.SetLongListMode(input_list)
            #If less than 20 or no summary allowed
            else: 
                for item in input_list:
                    self.AddLineEdit(string=item)
        #If we did not get a predefined list
        else:
            self.AddLineEdit()
    
    def OpenListPreset(self):
        #Ask load module for a list
        input_list = save_load.OpenFile()
        #If the cancel was not pressed
        if input_list is not None:
            #If it is not an empty list
            if len(input_list) > 0:
                self.SetList(input_list)

    def AddLineEdit(self, string=""):
        #If we want a resizable list
        if self.has_columns:
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
        #Give it a close button
        pixmap = QPixmap("/Users/sethvanderbijl/Coding Projects/Bible_features/app/close.png")
        btn = PicButton(pixmap)
        btn.setMaximumWidth(15)
        btn.setMaximumHeight(15)
        btn.clicked.connect(lambda x: self.RemoveEdit(edit))
        self.cur_layout.addWidget(btn, self.entries, self.column_num+1)

        #Whenever text is set of some cell manually update the hooked list
        if self.hooked_item != None:
            self.hooked_item.OnListValChange(self)
        
        #If we have line edits we are not a long list
        self.long_list=False

        #Traack entries to place new line at
        self.entries+=1
    
    def RemoveEdit(self, edit):
        #Only if there is more than one entry, we dont want an empty list
        if self.entries > 1:
            #Get current contents except for the current edit
            content = self.GetContents(exclude_edit=edit)

            #Set list
            self.SetList(content)

    def SetList(self, input_list):
        #First clear
        self.Clear()
        
        #If it is not a too long list
        if len(input_list) < 21 or not self.allow_summary:
            #Then
            for item in input_list:
                self.AddLineEdit(string=str(item).replace("\n", ""))
        #Else if it is to long render the list as longlistinfo
        elif self.allow_summary:
            print("setting long list")
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
    
    def GetContents(self, exclude_edit=None):
        #If we are in line edit mode
        if self.long_list == False:
            # Fill a list with the text contents of the edit fields
            l = []
            for edit in self.edits:
                if edit != exclude_edit:
                    l.append(edit.text())
            return l
        #If we are an uneditable long list
        else:
            #return the original supplied list
            return self.start_list

    def SetLongListMode(self, input_list=None):
        #Only displays information about the list if the list has too many items

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
        list_content_label = QLabel(total)

        #Wrap it so it spans multiple lines if needed
        list_content_label.setWordWrap(True)

        self.top_layout.addWidget(list_content_label)

        #We are now in longlist mode
        self.long_list=True

        self.start_list = input_list
