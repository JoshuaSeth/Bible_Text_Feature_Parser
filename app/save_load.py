import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *import dialog
import pandas as pd

def SetMainWindow(main_win):
    global main_window
    main_window = main_win

def _Save(object, save_name):
    with open(save_name, "wb") as fp:   #Pickling
        pickle.dump(object, fp)

def _Load(load_name):
    with open(load_name, "rb") as fp:   #Pickling
        b = pickle.load(fp)
    return b

def _LoadList(load_name):
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

    #If we have more than one column
    if data.shape[1] > 1:
        #Ask in a dialog to select a column
        cols = AskItems(data.columns)
    
    #Now put the columns after each other in a list
    list_data = []
    for col in cols:
        list_data.extend(data[col].tolist())

    return list_data


def OpenFile():
    fname = QFileDialog.getOpenFileName()
    return _LoadList(fname[0])

def AskItems(columns):
        dia = dialog.CustomDialog(main_window, columns)
        value = dia.exec_()
        if value:
            print(value)
        return value