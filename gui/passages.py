import pandas as pd
from divisions import Passage, Verse
from obsub import event

class Passages:
    def __init__(self):
        self.passages = [Passage("John 1:1 - John 1:3")]

    #Loads a list of passages and adds them to the current list
    def LoadPassageList(self, string):
        #Check for file type and load as df
        if string.contains(".xlsx"):
            pd.read_excel(string)
        if string.contains(".csv"):
            pd.read_csv(string)
        #Could add many more filetypes here

        #If there are multiple columns ask which column contains the divisions

        #Add every division in the column to the passages list

    #Add a passage to the current passage list
    def AddPassage(self,string):
        passage = Passage(string)
        self.passages.append(passage)
        self.OnListChanged()



    @event
    def OnListChanged(self):
        pass
