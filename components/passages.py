#This script handles the passages list
#Input should either be the current list to save it, an excel doc, an textfile, try:
#Output will always be a list [] with objects the progam can work with

from divisions import Passage, Verse

passages = []

#Loads a list of passages and adds them to the current list
def LoadPassageList(string):
    if string.contains(".xlsx"):
        print("opening excel")
    if string.contains(".csv"):
        print("opening csv")
    return None

#Add a passage to the current passage list
def AddPassage(string):
    passage = Passage(string)
    passages.append(passage)

print(Passage("John 1:1 - John 2:4").GetString())