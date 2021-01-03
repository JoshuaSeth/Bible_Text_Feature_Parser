from passages_pane import PassagePane
from plugins_pane import PluginsPane
from data_pane import DataPane
import run_pane
import bible
import pandas as pd
from table import DataFrameModel

def Scan():
    #Get access to the passage pane instance
    for pp in PassagePane.getinstances():
        passage_pane = pp
    
    #Get access to the plugins pane instance
    for pp in PluginsPane.getinstances():
        plugins_pane = pp

    #Get access to the data pane instance
    for dp in DataPane.getinstances():
        data_pane = dp

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

    #Set max value of prog bar to plugins times passages
    active_run_pane.pbar.setMaximum(num_plugins * total_rows)

    #Then send the last of passage df's to every plugin
    #Results we be a list of dicts with lists
    results = []
    #collect the data from all plugins
    for plugin in plugins_pane.active_plugins:
        data = plugin.ScanPassages(passages_dfs)
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

    #Send the results to the data pane
    data_pane.Display(df)