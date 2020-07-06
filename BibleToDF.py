import pandas as pd

def AddColumnWithLexeme(input):
    t = input['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕'].apply(SelectLexemeFromCell)
    input['v'] = t
    return input

def SelectLexemeFromCell(input):
    list = input.replace("〕", "").replace("〔", "").split("｜")
    return list[3]

def SelectOGNToFromCell(input):
    list = input.replace("〕", "").replace("〔", "").split("｜")
    return list[2]

def ExtractVerseAndWordColumn(input):
    return input[['〔Book｜Chapter｜Verse〕', '〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕']]


def GetLexemesForBibleBook(bibleBookNr, onlyLexemes):
    """Returns a dataframe of the bible book by number. When onlyLexemes is true it will return only greek lexeme words with their verses. Else it will return more data like strongs etc."""
    bibleData = pd.read_csv("bible.csv", sep='\t')

    bibleBook = bibleData[bibleData['〔Book｜Chapter｜Verse〕'].str.contains("〔"+str(bibleBookNr))]
    if not onlyLexemes:
        return bibleBook

    BibleBookLexemes = ExtractVerseAndWordColumn(bibleBook)
    BibleBookLexemes = AddColumnWithLexeme(BibleBookLexemes)
    return BibleBookLexemes