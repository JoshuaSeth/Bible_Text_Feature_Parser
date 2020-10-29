import weakref
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from divisions import Passage
from input_list import InputList

passages = ["John 17:1 - 17:3"]

class PassagePane(QGroupBox):

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

    def __init__(self,):
        #Register this instance
        self._instances.add(weakref.ref(self))

        #Initialize element
        super(PassagePane, self).__init__()

        #Give this widget a layout
        self.cur_layout = QVBoxLayout()
        self.setLayout(self.cur_layout)

        #The passages title
        label = QLabel("Passages")
        label.setFont(QFont('Arial', 28))
        qbox = QVBoxLayout()
        qbox.setAlignment(Qt.AlignCenter)
        qbox.addWidget(label)
        self.cur_layout.addLayout(qbox)

        self.passages_box=QVBoxLayout()
        self.cur_layout.addLayout(self.passages_box)
   

        #Make layout start at top instead of middle
        self.cur_layout.setAlignment(Qt.AlignTop)
        
        #Give the pane an input list for the passages
        self.list = InputList(passages)
        self.cur_layout.addWidget(self.list)

    def GetPassages(self, as_string=False):
        # Return a passage instance based on the input contents
        l = []
        for item in self.list.GetContents():
            if not as_string:
                l.append(Passage(item))
            else:
                l.append(Passage(item).GetString())
        return l




