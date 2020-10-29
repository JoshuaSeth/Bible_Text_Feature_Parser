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

    #Save a list of the df's of passages to send to the plugins
    passages_dfs = []
    for passage in passage_pane.GetPassages():
        df = bible.GetPassage(passage)
        passages_dfs.append(df)

    #Then send the last of passage df's to every plugin
    for plugin in plugins_pane.active_plugins:
        plugin.ScanPassages(passages_dfs)

    #By sending all passages instead of rows one can more easily debug per plugin
    #I.e. a plugin will break when it is its turn instead of everytime it gets a row