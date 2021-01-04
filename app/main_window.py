from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from passages_pane import PassagePane
from plugins_pane import PluginsPane
from run_pane import RunPane
from data_pane import DataPane
import dialog
import save_load
import os
import sys

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        #Call the super
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("My Awesome App")
        
        #Central layout and widget
        layout = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

        #Let save load know that this is the main window
        save_load.SetMainWindow(self)
        
        #Add costum widgets
        #Passage Pane
        pp = PassagePane()
        layout.addWidget(pp)

        #Plugin Pane
        plp = PluginsPane()
        layout.addWidget(plp)
        
        #Pane for layout and program
        run_data = QVBoxLayout()
        layout.addLayout(run_data)

        #Data Pane
        dp = DataPane()
        run_data.addWidget(dp)

        #Run program Pane
        rpp = RunPane()
        run_data.addWidget(rpp)

        #Make a menu bar
        # filling up a menu bar
        bar = self.menuBar()
        # File menu
        file_menu = bar.addMenu('File')
        # adding actions to file menu
        open_action = QAction('Open', self)
        open_action.setShortcuts(["Cmd+o", "Ctrl+o"])
        save_action = QAction('Save', self)
        save_action.setShortcuts(["Cmd+s, Ctrl+s"])
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        #Connect actions to closing and opening
        open_action.triggered.connect(lambda x=True: save_load.OpenFile(True))
        save_action.triggered.connect(lambda x=True: save_load.SaveFile(None))

        
basedir = os.path.dirname(sys.argv[0])
print(basedir)
# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication([])

window = MainWindow()
window.show() # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()

# Your application won't reach here until you exit and the event 
# loop has stopped.
