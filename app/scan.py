from passages_pane import PassagePane
from plugins_pane import PluginsPane
import run_pane
import bible
import pandas as pd
from table import DataFrameModel
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class ScanThread(QThread):
    current_results_buffer = None

    # Create a counter thread
    change_value = pyqtSignal(int)
    set_max = pyqtSignal(int)
    finish_signal = pyqtSignal(QThread)
    def run(self):
        self.current_results_buffer = RunScan(thread=self)  
        self.finish_signal.emit(self)



def RunScan(thread=None):
    #Get access to the passage pane instance
    for pp in PassagePane.getinstances():
        passage_pane = pp
    
    #Get access to the plugins pane instance
    for pp in PluginsPane.getinstances():
        plugins_pane = pp

    #Save a list of the df's of passages to send to the plugins
    passages_dfs = []
    for passage in passage_pane.GetPassages():
        df = bible.GetPassage(passage)
        passages_dfs.append(df)
    
    #Set the progress bar max value
    #Get the run pane
    for t  in run_pane.RunPane.getinstances():
        active_run_pane = t

    #Get the number of plugins running on the data times the amount of passages times rows per df
    num_plugins = len(plugins_pane.active_plugins)
    total_rows = 0
    for passage_df in passages_dfs:
        total_rows+=len(passage_df)
        print(len(passage_df))

    #Set max value of prog bar to plugins times passages
    thread.set_max.emit(num_plugins * total_rows)

    #Then send the last of passage df's to every plugin
    #Results we be a list of dicts with lists
    results = []
    #collect the data from all plugins
    for plugin in plugins_pane.active_plugins:
        data = plugin.ScanPassages(passages_dfs, thread=thread)
        results.append(data)

    #By sending all passages instead of rows one can more easily debug per plugin
    #I.e. a plugin will break when it is its turn instead of everytime it gets a row

    #Create a dataframe
    df = pd.DataFrame()

    #Assign the passages
    df ["Passages"] = passage_pane.GetPassages(as_string=True)

    #Now for each list in the dataas of the plugins assign it to the dataframe
    for data in results:
        #Get the header and list to make a colum
        if data is not None:
            for header, list_val in data.items():
                print(header, list_val)
                df[header] = list_val

    return df