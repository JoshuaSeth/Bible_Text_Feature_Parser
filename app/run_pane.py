from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from input_list import InputList
from data_pane import DataPane
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

        self.cur_layout.addWidget(self.pbar)   
        

        #Connect it to running the script
        self.run.clicked.connect(self.StartScan)

        self.cur_layout.addWidget(self.run)
    

    def StartScan(self):
        self.pbar.setValue(0)
        self.thread = scan.ScanThread()
        self.thread.change_value.connect(self.SetProgressVal)
        self.thread.set_max.connect(self.SetMaxVal)
        self.thread.finish_signal.connect(self.DisplayResults)
        self.thread.start()

    def DisplayResults(self, val):
        #Get results from the thread
        current_results_buffer = val.current_results_buffer

        #Get access to the data pane instance
        for dp in DataPane.getinstances():
            data_pane = dp
        
        #Send the results to the data pane
        data_pane.Display(current_results_buffer)

    def SetProgressVal(self, val):
        print(self.pbar.value())
        self.pbar.setValue(self.pbar.value() + val)
    
    def SetMaxVal(self, val):
        self.pbar.setMaximum(val)
  

    