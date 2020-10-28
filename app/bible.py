import pandas as pd

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
    return int(split[0])

#Get bible chapter ftom〔Book｜Chapter｜Verse〕
def GetChapter(input):
    #Get split version
    split = GetBookChapterVerseSplit(input)

    #Returns chapter
    return int(split[1])

#Get bible verse from 〔Book｜Chapter｜Verse〕
def GetVerse(input):
    #Get split
    split = GetBookChapterVerseSplit(input)

    #Returns verse
    return int(split[2])

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
    return bible.loc[bible['Book']== bible_book_nr]

def GetBibleVerse(verse):
    book = bible.loc[bible['Book'] == verse.book]
    chapter = book.loc[book['Chapter'] == verse.chapter]
    verse = chapter.loc[chapter['Verse'] == verse.verse]
    return verse

def GetPassage(passage):
    #EXAMPLE: JOHN 3:6 - ROMANS 5:4

    #All the books this is in
    #JOHN - ACTS - ROMANS
    books = bible.loc[bible['Book'].between(passage.start.book, passage.end.book)]

    #First book
    #JOHN
    first_book = books.loc[books['Book'] == passage.start.book]

    #Last book
    #ROMANS
    last_book = books.loc[books['Book'] == passage.end.book]

    #books between
    #ACTS
    books_between = books.loc[books['Book'].between(passage.start.book, passage.end.book, inclusive=False)]

    #Get the last chapters of the first book
    #JOHN 4 - 21
    first_book_chapters = first_book.loc[first_book['Chapter'].between(passage.start.chapter, 999, inclusive=False)]

    #Get the first chaptes of the last book
    #ROMANS 1 - 4
    last_book_chapters = last_book.loc[last_book['Chapter'].between(-1, passage.end.chapter, inclusive=False)]
    
    #Get all the chapters in tbween this
    #ACTS
    between_chapters = books_between

    #Get the first chapter of the first book
    #JOHN 3
    first_book_first_chapter = first_book.loc[first_book["Chapter"] == passage.start.chapter]

    #Get the last verses of this chapter
    #JOHN 3:5-21
    first_b_c_verses = first_book_first_chapter.loc[first_book_first_chapter["Verse"].between(passage.start.verse, 999)]

    #Get the last chapter of the last book
    #ROMANS 5
    last_book_last_chapter = last_book.loc[last_book["Chapter"] == passage.end.chapter]

    #Get the first verses of this chapter
    #ROMANS 5:1-4
    last_b_c_verses =  last_book_last_chapter.loc[last_book_last_chapter["Verse"].between(0, passage.end.verse)]

    #Now concantenate them to the relevant passage
    #JOHN 3:5-21 + JOHN 4-21 + ACTS + ROMANS 1-4 + ROMANS 5:1-4
    frames = [first_b_c_verses, first_book_chapters, between_chapters, last_book_chapters, last_b_c_verses]

    return pd.concat(frames)




    
    verses


def GetBible():
    return bible


########################################################################
#VARIABLES
bible = _LoadBible()