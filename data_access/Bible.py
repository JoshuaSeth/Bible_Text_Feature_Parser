import pandas as pd
from data_access import PassageParser as pps

########################################################################
#PANDAS HELPER FUNCTIONS

#Get the lexeme of the Greek word
def GetLexeme(input):
    split = input.replace("〕", "").replace("〔", "").split("｜")
    return split[3]

#Get the Open Greek New Testament Word
def GetGreekWord(input):
    split = input.replace("〕", "").replace("〔", "").split("｜")
    return split[2]

#Get Bible book from 〔Book｜Chapter｜Verse〕
def GetBook(input):
    #Get split version
    split = GetBookChapterVerseSplit(input)

    #Returns book,
    return split[0]

#Get bible chapter ftom〔Book｜Chapter｜Verse〕
def GetChapter(input):
    #Get split version
    split = GetBookChapterVerseSplit(input)

    #Returns chapter
    return split[1]

#Get bible verse from 〔Book｜Chapter｜Verse〕
def GetVerse(input):
    #Get split
    split = GetBookChapterVerseSplit(input)

    #Returns verse
    return split[2]

def GetBookChapterVerseSplit(input):
    #Remove brackers
    clean_input = str(input).replace("〔", "").replace("〕", "")

    #Split into book chapter verses
    split = clean_input.split("｜")

    return split

########################################################################
#FUNCTIONS

#Get a clean DF for the whole NT
def _LoadBible():
    #Read the bibleData csv into pandas
    bible_data = pd.read_csv("data/bible.csv", sep='\t')

    #Select the 〔Book｜Chapter｜Verse〕column
    column = bible_data["〔Book｜Chapter｜Verse〕"]

    #Add a book chapter verse columns
    bible_data["Book"] = column.apply(GetBook)

    #Add a book chapter verse columns
    bible_data["Chapter"] = column.apply(GetChapter)

    #Add a book chapter verse columns
    bible_data["Verse"] = column.apply(GetVerse)

    #Drop the old bible chapter verse column
    bible_data = bible_data.drop('〔Book｜Chapter｜Verse〕', 1)

    #Select the column with wordsd
    word_column = bible_data['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕']

    #Get the greek word
    bible_data["Greek Word"] = word_column.apply(GetGreekWord)

    #Get the lexeme 
    bible_data["Lexeme"] = word_column.apply(GetLexeme)

    #Only save the relevant columns
    bible_data = bible_data[["Book", "Chapter", "Verse", "Greek Word", "Lexeme"]]

    return bible_data


def GetBookDF(bible_book_nr):
    return bible.loc[bible['Book']==str(bible_book_nr)]

def GetBible():
    return bible


########################################################################
#VARIABLES
bible = _LoadBible()