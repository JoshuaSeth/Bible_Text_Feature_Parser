from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from passages import Passages

class PassagePane(QGroupBox):
    def __init__(self):
        #Initialize element
        super(PassagePane, self).__init__()

        #Initiliaze the passage data class
        self.passages = Passages()

        #Give this widget a layout
        self.cur_layout = QVBoxLayout()
        self.setLayout(self.cur_layout)

        #Make layout start at top instead of middle
        self.cur_layout.setAlignment(Qt.AlignTop)

        #Render it a first time
        self.Render()

        #Rerender it everytime the passages data changes
        self.passages.OnListChanged += self.Render
        
    #Rerenders the contents based on the current passages in the list
    def Render(self, args=[]):
        # Empty the layout
        for i in reversed(range(self.cur_layout.count())): 
            self.cur_layout.itemAt(i).widget().deleteLater()

        #Give the layouts items
        for passage in self.passages.passages:
            name = passage.GetString()
            self.cur_layout.addWidget(PassageUI(name))
        
        #Add the bottom a text field and button to add passages
        self.cur_layout.addWidget(AddPassageBtn(self))


#A button that allows you to write a passage and add it
class AddPassageBtn(QWidget):
    def __init__(self, parent):
        super(AddPassageBtn, self).__init__()

        #Give this widget a layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        #Write the label of the passage
        self.text = QLineEdit()
        layout.addWidget(self.text)

        #Add a 'add' Button
        self.bt1 = QPushButton("Add")
        layout.addWidget(self.bt1)

        #Adds a button that can add a passage to the list
        self.bt1.clicked.connect(lambda x: parent.passages.AddPassage(self.text.text()))

#Ui for showing a passage with a delete and edit knob
class PassageUI(QWidget):
    def __init__(self, string):
        super(PassageUI, self).__init__()

        #Give this widget a layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        #Write the label of the passage
        text = QLabel(string)
        layout.addWidget(text)

        #Add the necessary buttons
        bt1 = QPushButton("+")
        bt2 = QPushButton("-")
        bt3 = QPushButton("x")

        icon = QIcon.fromTheme("edit.png")
        bt1.setIcon(icon)
        bt1.setIconSize(QSize(24,24))

        layout.addWidget(bt1)
        layout.addWidget(bt2)
        layout.addWidget(bt3)