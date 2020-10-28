from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from input_list import InputList
import os
import scan

class RunPane(QGroupBox):
    def __init__(self):
        #Initialize element
        super(RunPane, self).__init__()

        #Give this widget a layout
        self.cur_layout = QVBoxLayout()
        self.setLayout(self.cur_layout)
        self.cur_layout.setAlignment(Qt.AlignTop)

        #The run title
        label = QLabel("Run Program")
        label.setFont(QFont('Arial', 28))
        qbox = QVBoxLayout()
        qbox.setAlignment(Qt.AlignCenter)
        qbox.addWidget(label)
        self.cur_layout.addLayout(qbox)

        self.run = QPushButton("Run")

        #Connect it to running the script
        self.run.clicked.connect(scan.Scan)

        self.cur_layout.addWidget(self.run)