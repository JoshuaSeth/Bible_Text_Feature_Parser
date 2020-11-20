from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from passages_pane import PassagePane
from plugins_pane import PluginsPane
from run_pane import RunPane
from data_pane import DataPane
import dialog
import save_load

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
        
        #Run program Pane
        rpp = RunPane()
        layout.addWidget(rpp)

        #Data Pane
        dp = DataPane()
        layout.addWidget(dp)

        #Check for some basic keys
        #Saving
        save_sc_ctrl = QShortcut(QKeySequence("Ctrl+S"), self)
        save_sc_ctrl.activated.connect(save_load.SaveFile)
        save_sc_cmd = QShortcut(QKeySequence("Cmd+S"), self)
        save_sc_cmd.activated.connect(save_load.SaveFile)

        #Opening
        open_sc_ctrl = QShortcut(QKeySequence("Ctrl+O"), self)
        open_sc_ctrl.activated.connect(lambda x=True: save_load.OpenFile(x))
        open_sc_cmd = QShortcut(QKeySequence("Cmd+O"), self)
        open_sc_cmd.activated.connect(lambda x=True: save_load.OpenFile(x))

        

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
