import book_names as bn
import re

class Verse:
    def __init__(self, string="", previous_verse=None, row=None):
        #If a string was passaed
        if string != "":
            #Construct it from a string
            self.CreateFromString(string, previous_verse)
        #Else if a dataframe row was passed
        elif row != None:
            #Get the data from the relevant columns
            self.book = int(row[1])
            self.chapter = int(row[2])
            self.verse = int(row[3])
            self.book_name = bn.books[self.book]
            self.post_fix = ""


    def CreateFromString(self, string, previous_verse):
        #Check the structure of the string
        has_spaces = string.__contains__(" ")
        has_separator = string.__contains__(":")

        #Book
        #If no book name is given assume book name of previous verse
        if not has_spaces:
            self.book_name = previous_verse.book_name
        #Else get the name of the bible book
        else:
            self.book_name = string.split(" ")[0]

        #Book nr
        #Get the number key for the name value
        self.book = int(bn.GetBookNr(self.book_name))

        #Chapter
        if not has_spaces:
            #If there is also no :
            if not has_separator:
                self.chapter = previous_verse.chapter
            #If there is no space but is :
            else:
                self.chapter = int(string.split(":")[0])
        #Chapter is the part before(:)
        else:
            self.chapter = int(string.split(" ")[1].split(":")[0])

        #Verse
        #The string might be just the verse
        if not has_separator:
            verse_item = string
        #If its more, then select the verse part
        else:
            verse_item = string.split(":")[1]

        #Get the number part as the verse: 2
        self.verse = int(re.sub("[^0-9]", "",verse_item))

        #Get the non number part as the postfix : b
        self.post_fix = ''.join(c for c in verse_item if not c.isdigit())
    
    #Return this verse as a formatted string
    def GetString(self):
        return bn.books[self.book] + " " + self.GetChapterVerse()
    
    #Returns only the chapter and verse
    def GetChapterVerse(self):
        return str(self.chapter) + ":" + str(self.verse) + str(self.post_fix)


class Passage:
    def __init__(self, string):
        #Split the string in an start and end verse
        split = string.split("-")
        start_verse_str = split[0].lstrip().rstrip()
        end_verse_str = split[1].lstrip().rstrip()

        #Parse both verse strings to 
        start_verse = Verse(start_verse_str)
        end_verse = Verse(end_verse_str, start_verse)

        #Assign them to this passage
        self.start = start_verse
        self.end = end_verse
    
    #Return passage as a formatted string
    def GetString(self):
        #The start is always the start string
        string = self.start.GetString()

        #Add midpart
        string+="-"

        #If the bible books are different: John 1:1 - Acts 4:14
        if self.start.book != self.end.book:
            string+=self.end.GetString()
        
        #If only the chapter is different: John 1:1- 4:14
        elif self.start.chapter != self.end.chapter:
            string+=self.end.GetChapterVerse()

        #If only the endverse is different John 1:1 - 10
        else:
            string+=str(self.end.verse)+self.end.post_fix

        return string