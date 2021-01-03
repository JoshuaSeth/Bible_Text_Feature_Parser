from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from input_list import InputList
import os
import scan
import weakref

class RunPane(QGroupBox):
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
        super(RunPane, self).__init__()

        #Give this widget a layout
        self.cur_layout = QHBoxLayout()
        self.setLayout(self.cur_layout)
        self.cur_layout.setAlignment(Qt.AlignRight)

        #The run title
        qbox = QVBoxLayout()
        qbox.setAlignment(Qt.AlignCenter)
        self.cur_layout.addLayout(qbox)

        self.run = QPushButton("Run")
        self.run.setMaximumWidth(200)
        self.run.setMinimumWidth(200)

        # creating progress bar 
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
  
        # setting its geometry 
        # self.pbar.setGeometry(0, 0, 200, 25) 

        self.cur_layout.addWidget(self.pbar)   
            

        #Connect it to running the script
        self.run.clicked.connect(scan.Scan)

        self.cur_layout.addWidget(self.run)