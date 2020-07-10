import pandas as pd
import PassageParser as pps

def AddLexemeAndWordColumn(input):
    lexemeColumn = input['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕'].apply(SelectLexemeFromCell)
    input['v'] = lexemeColumn
    OGNToColumn = input['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕'].apply(SelectOGNToFromCell)
    input['ognto'] = OGNToColumn
    CodeColumn = input['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕'].apply(SelectCodeFromCell)
    input['code'] = CodeColumn
    KeyColumn = input['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕'].apply(SelectKeyFromCell)
    input['morphKey'] = KeyColumn
    return input

def SelectCodeFromCell(input):
    list = input.replace("〕", "").replace("〔", "").split("｜")
    return list[4]

def SelectLexemeFromCell(input):
    list = input.replace("〕", "").replace("〔", "").split("｜")
    return list[3]

def SelectKeyFromCell(input):
    list = input.replace("〕", "").replace("〔", "").split("｜")
    return list[5]

def SelectOGNToFromCell(input):
    list = input.replace("〕", "").replace("〔", "").split("｜")
    return list[2]

def ExtractVerseAndWordColumn(input):
    return input[['〔Book｜Chapter｜Verse〕', '〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕']]

def GetLexemesForDivision(divisionString):
    """Returns a dataframe of the bible book by number. When onlyLexemes is true it will return only greek lexeme words with their verses. Else it will return more data like strongs etc."""
    bibleData = pd.read_csv("bible.csv", sep='\t')

    parsedDivision = pps.DivisionToBCVStringList(divisionString)

    collectedRows = None

    for VerseCode in parsedDivision:
        relevantRows = bibleData[bibleData['〔Book｜Chapter｜Verse〕'].str.contains(VerseCode)]
        if collectedRows is None:
            collectedRows=relevantRows
        else:
            dfCollection = [collectedRows, relevantRows]
            collectedRows = pd.concat(dfCollection)


    RelevantRowsLexemes = ExtractVerseAndWordColumn(collectedRows)
    RelevantRowsLexemes = AddLexemeAndWordColumn(RelevantRowsLexemes)
    return RelevantRowsLexemes


def GetLexemesForBibleBook(bibleBookNr, onlyLexemes):
    """Returns a dataframe of the bible book by number. When onlyLexemes is true it will return only greek lexeme words with their verses. Else it will return more data like strongs etc."""
    bibleData = pd.read_csv("bible.csv", sep='\t')

    bibleBook = bibleData[bibleData['〔Book｜Chapter｜Verse〕'].str.contains("〔"+str(bibleBookNr))]
    if not onlyLexemes:
        return bibleBook

    BibleBookLexemes = ExtractVerseAndWordColumn(bibleBook)
    BibleBookLexemes = AddLexemeAndWordColumn(BibleBookLexemes)
    return BibleBookLexemes

def GetALLNTLexemes():
    bibleData = pd.read_csv("bible.csv", sep='\t')
    bibleLexemes = ExtractVerseAndWordColumn(bibleData)
    bibleLexemes = AddLexemeAndWordColumn(bibleLexemes)
    return bibleLexemes