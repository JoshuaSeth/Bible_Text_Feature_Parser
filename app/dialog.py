from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from check_combo_box import CheckableComboBox



class CustomDialog(QDialog):
    
    def __init__(self, main_window, columns):

        super(CustomDialog, self).__init__()

        self.setWindowTitle("Please select your option(s)")

        print('running dialog')

        self.layout = QVBoxLayout(self)
        super(CustomDialog, self).setLayout(self.layout)
        self.cbb = CheckableComboBox(columns)
        self.layout.addWidget(self.cbb)

        #buttons
        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.Accept)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.Reject)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
    
    def Accept(self):
        self.accept = True
    
    def Reject(self):
        self.accept = False

    def exec_(self):
        super(CustomDialog, self).exec_()
        return self.cbb.GetContent(), self.accept