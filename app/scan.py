from passages_pane import PassagePane
from plugins_pane import PluginsPane
import bible

def Scan():
    #Get access to the passage pane instance
    for pp in PassagePane.getinstances():
        passage_pane = pp
    
    #Get access to the plugins pane instance
    for pp in PluginsPane.getinstances():
        plugins_pane = pp

    for passage in passage_pane.GetPassages():
        df = bible.GetPassage(passage)
        for row in df.iterrows():
            for plugin in plugins_pane.active_plugins:
                plugin.Note(row)


