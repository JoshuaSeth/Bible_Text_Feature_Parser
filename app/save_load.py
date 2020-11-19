import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd

def _Save(object, save_name):
    with open(save_name, "wb") as fp:   #Pickling
        pickle.dump(object, fp)

def _Load(load_name):
    with open(load_name, "rb") as fp:   #Pickling
        b = pickle.load(fp)
    return b

def _LoadList(load_name):
    if load_name.endswith(".txt"):
        data = pd.read_csv(load_name, sep = None, engine='python')
    if load_name.endswith(".xlsx"):
        data = pd.read_excel(load_name)
    print("shape:",data.shape)
    print(data.iloc[:, 1].tolist())
    print(data.iloc[:, 2].tolist())
    return data.iloc[:, 0].tolist()


def OpenFile():
    fname = QFileDialog.getOpenFileName()
    return _LoadList(fname[0])