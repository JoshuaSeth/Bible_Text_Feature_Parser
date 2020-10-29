from passages_pane import PassagePane
from plugins_pane import PluginsPane
from data_pane import DataPane
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
                print(list_val)
                df[header] = list_val

    #Send the results to the data pane
    data_pane.Display(df)