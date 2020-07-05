import pandas as pd

def AddColumnWithLexeme(input):
    t = input['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕'].apply(SelectLexemeFromCell)
    input['v'] = t
    return input

def SelectLexemeFromCell(input):
    return input.replace("〕", "").replace("〔", "").split("｜")[3]


def ExtractVerseAndWordColumn(input):
    return input[['〔Book｜Chapter｜Verse〕', '〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕']]

def GetVerseAndLexemeDF():
    bibleData = pd.read_csv("bible.csv", sep='\t')
    print(bibleData)
    #COMMENTED OUT SINCE WE DO IT NOW ONLY FOR JOHNS GOSPEL
    # bibleDataVersesAndWords = ExtractVerseAndWordColumn(bibleData)
    # bibleDataVersesAndWords = AddColumnWithSingleWord(bibleDataVersesAndWords)

    #Whenever something is part of chapter 43 it is Johns gospel, select all rows with 〔43 as chapter in their column
    gJohnData = bibleData[bibleData['〔Book｜Chapter｜Verse〕'].str.contains("〔43")]
    GJohnVerseAndLexeme = ExtractVerseAndWordColumn(gJohnData)
    GJohnVerseAndLexeme = AddColumnWithLexeme(GJohnVerseAndLexeme)
    return GJohnVerseAndLexeme