import weakref
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from table import DataFrameModel

class DataPane(QGroupBox):

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
        super(DataPane, self).__init__()

        #Give this widget a layout
        self.cur_layout = QVBoxLayout()
        self.setLayout(self.cur_layout)

        #The passages title
        label = QLabel("Data")
        label.setFont(QFont('Arial', 28))
        qbox = QVBoxLayout()
        qbox.setAlignment(Qt.AlignCenter)
        qbox.addWidget(label)
        self.cur_layout.addLayout(qbox)

        self.data_box=QVBoxLayout()
        self.cur_layout.addLayout(self.data_box)
   

        #Make layout start at top instead of middle
        self.cur_layout.setAlignment(Qt.AlignTop)
        
        #Give the pane a table with the data
        self.table_view = QTableView()
        self.cur_layout.addWidget(self.table_view)

    def Display(self, df):
        #Convert the dataframe to a PYQt table
        model = DataFrameModel(df)

        self.table_view.setModel(model)