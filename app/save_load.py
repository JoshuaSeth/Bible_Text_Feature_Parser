import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import dialog
import pandas as pd
from workspace import WorkSpace
import passages_pane
import plugins_pane
import data_pane

def SetMainWindow(main_win):
    global main_window
    main_window = main_win

def OpenFile(is_workspace=False):
    if not is_workspace:
        fname = QFileDialog.getOpenFileName()
        #If the cancel button wasn pressed
        if fname is not None:
            return _LoadList(fname[0])
        else:
            return None
    else:
        filters = "Workspaces (*.workspace)"
        selected_filter = "Workspaces (*.workspace)"
        fname = QFileDialog.getOpenFileName(filter=filters,initialFilter= selected_filter)
        #If the cancel button wasn pressed
        if fname is not None:
            fname = fname[0]
            _OpenWorkspace(fname)

def SaveFile(save_file=None):
    #If it is a list or dataframe save it with the pandas saving method
    if type(save_file) is list or type(save_file) is pd.DataFrame:
        _SaveList(save_file)
    if save_file is None:
        _SaveWorkspace()

def _SaveWorkspace():
    #Create a new workspace object to save
    ws = WorkSpace()
    #Get access to the passage pane instance
    for pp in passages_pane.PassagePane.getinstances():
        pasages = pp
    ws.__dict__["Passages"] = pp.GetPassages(parsed=False)
    #Get access to the plugins pane instance
    for ppa in plugins_pane.PluginsPane.getinstances():
        plugins = ppa
    ws.__dict__["Plugins"] = []
    for plugin in ppa.active_plugins:
        ws.__dict__["Plugins"].append(plugin.GetAsDict())

    #Get the location for the save
    filters = "Workspaces (*.workspace)"
    selected_filter = "Workspaces (*.workspace)"
    name, file_type = QFileDialog.getSaveFileUrl()
    name = name.path()
    #Save the workspace
    _Save(ws, name)

def _OpenWorkspace(fname):
    #Open a workspace to the panes
    ws = _Load(fname)
    print(ws.__dict__)

    #Get access to the passage pane instance
    for pp in passages_pane.PassagePane.getinstances():
        passage_pane = pp
    #Load the passages into the pane
    pp.SetPassages(ws.__dict__["Passages"])

    #Load the plugins pane
    for ppa in plugins_pane.PluginsPane.getinstances():
        plugins = ppa
    
    #Open the plugins that were saved
    ppa.LoadPluginsFromWorkspace(ws)
    

def _Save(object, save_name):
    with open(save_name, "wb") as fp:   #Pickling
        pickle.dump(object, fp)

def _Load(load_name):
    with open(load_name, "rb") as fp:   #Pickling
        b = pickle.load(fp)
    return b

def _LoadList(load_name):
    data = None
    if load_name.endswith(".txt") or load_name.endswith(".csv"):
        data = pd.read_csv(load_name, sep = None, engine='python')
    if load_name.endswith(".xlsx"):
        data = pd.read_excel(load_name)
    if load_name.endswith(".feather"):
        data = pd.read_feather(load_name)
    if load_name.endswith(".fwf"):
        data = pd.read_fwf(load_name)
    if load_name.endswith(".gbq"):
        data = pd.read_gbq(load_name)
    if load_name.endswith(".html"):
        data = pd.read_html(load_name)
    if load_name.endswith(".json"):
        data = pd.read_json(load_name)
    if load_name.endswith(".orc"):
        data = pd.read_orc(load_name)
    if load_name.endswith(".parquet"):
        data = pd.read_parquet(load_name)
    if load_name.endswith(".pickle"):
        data = pd.read_pickle(load_name)
    if load_name.endswith(".sas"):
        data = pd.read_sas(load_name)
    if load_name.endswith(".spss"):
        data = pd.read_spss(load_name)
    if load_name.endswith(".stata"):
        data = pd.read_stata(load_name)
    if load_name.endswith(".hdf"):
        data = pd.read_hdf(load_name)
    if load_name.endswith(".table"):
        data = pd.read_table(load_name)
    if load_name.endswith(".sql"):
        data = pd.read_sql(load_name)

    #Might be because of cancel button
    if type(data) != pd.DataFrame:
        return None

    #If we have more than one column
    if data.shape[1] > 1:
        #Ask in a dialog to select a column
        cols = _AskItems(data.columns)
    
    #Now put the columns after each other in a list
    list_data = []
    if cols is not None:
        for col in cols:
            list_data.extend(data[col].tolist())

    return list_data

def _SaveList(input_list):
    df = pd.DataFrame(input_list)
    name, file_type = QFileDialog.getSaveFileUrl()
    name = name.path()
    print(name)
    if name.endswith(".xlsx"):
        df.to_excel(name, index=False)
    if name.endswith(".csv") or name.endswith(".txt"):
        df.to_csv(name, index=False)
    if name.endswith(".feather"):
        df.to_feather(name, index=False)
    if name.endswith(".gbq"):
        df.to_gbq(name, index=False)
    if name.endswith(".hdf5"):
        df.to_hdf(name, index=False)
    if name.endswith(".html"):
        df.to_html(name, index=False)
    if name.endswith(".tex"):
        df.to_latex(name, index=False)
    if name.endswith(".json"):
        df.to_json(name, index=False)
    if name.endswith(".md"):
        df.to_markdown(name, index=False)
    if name.endswith(".dta"):
        df.to_stata(name, index=False)
    if name.endswith(".sql"):
        df.to_sql(name, index=False)
    if name.endswith(".records"):
        df.to_records(name, index=False)
    if name.endswith(".pickle") or name.endswith(".bzip") or name.endswith(".gzip") or name.endswith(".bz2") or name.endswith(".zip") or name.endswith(".xz"):
        df.to_pickle(name, index=False)

def _AskItems(columns):
        value, ok = dialog.CustomDialog(main_window, columns).exec_()
        if not ok:
            return None
        return value