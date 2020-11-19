from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from check_combo_box import CheckableComboBox



class CustomDialog(QInputDialog):
    
    def __init__(self, main_window, columns):

        super(CustomDialog, self).__init__()

        self.setWindowTitle("HELLO!")

        print('running dialog')


        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel('yey')
        self.layout.addWidget(self.label)

        self.cbb = CheckableComboBox(columns)

        self.layout.addWidget(self.cbb)

    def exec_(self):
        super(CustomDialog, self).exec_()
        return self.cbb.GetContent()