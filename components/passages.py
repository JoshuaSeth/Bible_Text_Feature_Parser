import pandas as pd

from divisions import Passage, Verse

passages = []

#Loads a list of passages and adds them to the current list
def LoadPassageList(string):
    #Check for file type and load as df
    if string.contains(".xlsx"):
        pd.read_excel(string)
    if string.contains(".csv"):
        pd.read_csv(string)
    #Could add many more filetypes here

    #If there are multiple columns ask which column contains the divisions

    #Add every division in the column to the passages list

#Add a passage to the current passage list
def AddPassage(string):
    passage = Passage(string)
    passages.append(passage)

print(Passage("John 1:1 - John 2:4").GetString())