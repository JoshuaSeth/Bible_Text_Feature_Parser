import pandas as pd
from string import ascii_letters
import MarkupReader as mur
import Strongs
import Terms as t
import pickle

#Initial Code

def ExtractVerseAndWordColumn(input):
    return input[['〔Book｜Chapter｜Verse〕', '〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕']]

def SelectLexemeFromCell(input):
    return input.replace("〕", "").replace("〔", "").split("｜")[3]

def AddColumnWithLexeme(input):
    t = input['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕'].apply(SelectLexemeFromCell)
    input['v'] = t
    return input

def DivisionToBibleBookString(book):
    asList= book.replace("〕", "").replace("〔", "").split("｜")
    string = "JHN "
    string = string + asList[1]+":" +asList[2]
    return string


def DivisionToBCVString(division):
    division = str(division)
    division =division.replace(")", "")
    division =division.replace("(", "")
    division = ''.join(c for c in division if c not in ascii_letters)
    BCVString = []
    chapterVersesSplit = division.split(":")
    if(chapterVersesSplit[1].__contains__('-')):
        verses = chapterVersesSplit[1].split("-")
        string = "〔43｜"
        for versNr in range(int(verses[0]), int(verses[1])+1):
            BCVString.append(string+chapterVersesSplit[0]+"｜"+str(versNr)+"〕")
    else:
        string = "〔43｜"
        BCVString.append(string + chapterVersesSplit[0] + "｜" + str(chapterVersesSplit[1]) + "〕")
    return BCVString

def GetData(sequence, onlyWordCount):
    #Check if it is a valid sequence
    print(sequence)
    if pd.isna(sequence):
        print("Error, a NAN found, skipping this sequence")
        return None

    #Count Propositions, preference terms and, de/oun ratios

    #Johaninne Preference Words
    ptCount = {}
    if (not onlyWordCount):
        for term in t.terms:
            ptCount[term] = 0

    #Propositions
    prpCount = {}
    if (not onlyWordCount):
        for term in t.prepositions:
            prpCount[term] = 0

    #De/Oun
    deounCount = {}
    if (not onlyWordCount):
        for term in t.deounlist:
            deounCount[term] = 0

    featureCount = {}
    featureCount["Hapax Legomena"] = 0
    featureCount["Compound Words"] = 0
    featureCount["Foreign Words"] = 0
    featureCount["Historical Present"] = 0

    sequenceTotalWords = 0
    parsedSequence = DivisionToBCVString(sequence)


    for verseTag in parsedSequence:
        #Select all rows from df which are part of this verse
        rowsForVerse = GJohnVerseAndLexeme.loc[GJohnVerseAndLexeme['〔Book｜Chapter｜Verse〕'] == verseTag]
        sequenceTotalWords += len(rowsForVerse)

        if(not onlyWordCount):
            #Historical presents are counted for the whole verse so not per word row of the verse
            featureCount['Historical Present'] += mur.MarkUpContainsHistoricalPresent(
                DivisionToBibleBookString(verseTag))

            for wordRow in rowsForVerse.itertuples():
                greekWord = wordRow[3]
                count = len(GJohnVerseAndLexeme[GJohnVerseAndLexeme['v'] == str(greekWord)])
                if count < 2:
                    featureCount['Hapax Legomena']+=1
                if Strongs.compoundWords.__contains__(greekWord):
                    featureCount['Compound Words']+=1
                    print(greekWord + " is a compound")
                if Strongs.foreignWords.__contains__(greekWord):
                    if(not greekWord.__contains__('Ἰησοῦς')):
                        featureCount['Foreign Words']+=1
                        print(greekWord + " is a foreign word")

                if ptCount.__contains__(greekWord):
                    ptCount[greekWord]+=1
                if prpCount.__contains__(greekWord):
                    prpCount[greekWord]+=1
                if deounCount.__contains__(greekWord):
                    deounCount[greekWord]+=1

    metadata = {}
    metadata['Passage'] = sequence
    metadata['Word Count'] = sequenceTotalWords


    return [metadata, featureCount, deounCount ,prpCount, ptCount]




class Chapter():
    def __init__(self):
        self.index = 0
        self.hapaxes = []

def GetVerseAndLexemeDF():
    global GJohnVerseAndLexeme
    bibleData = pd.read_csv("bible.csv", sep='\t')
    #COMMENTED OUT SINCE WE DO IT NOW ONLY FOR JOHNS GOSPEL
    # bibleDataVersesAndWords = ExtractVerseAndWordColumn(bibleData)
    # bibleDataVersesAndWords = AddColumnWithSingleWord(bibleDataVersesAndWords)

    #Whenever something is part of chapter 43 it is Johns gospel, select all rows with 〔43 as chapter in their column
    gJohnData = bibleData[bibleData['〔Book｜Chapter｜Verse〕'].str.contains("〔43")]
    GJohnVerseAndLexeme = ExtractVerseAndWordColumn(gJohnData)
    GJohnVerseAndLexeme = AddColumnWithLexeme(GJohnVerseAndLexeme)


GetVerseAndLexemeDF()

sequencesList = pd.read_excel('outline_John_kopie.xlsx')
verseDivisionList = sequencesList["Morris"]

#print(ParseSequence(morrisSequence[3]))
datasForPassages = {}
for sequence in verseDivisionList:
    data= GetData(sequence)
    if data is not None:
        wordCount = data[0]["Word Count"]
        print(wordCount)
        dictInd = 0
        for dictionary in data:
            dictInd +=1
            for dataPointKey, dataPointVal in dictionary.items():
                newKey = str(dictInd) + ": " + str(dataPointKey)
                ratioKey = str(dictInd) + ": " + str(dataPointKey) + " ratio"
                if not datasForPassages.__contains__(newKey):
                    datasForPassages[newKey] = []
                datasForPassages[newKey].append(dataPointVal)

                #Ratio's
                if isinstance(dataPointVal, int):
                    if not datasForPassages.__contains__(ratioKey):
                        datasForPassages[ratioKey] = []
                    if dataPointVal != 0 and wordCount!=0:
                        datasForPassages[ratioKey].append(dataPointVal/wordCount)
                    else:
                        datasForPassages[ratioKey].append(0)
    print(datasForPassages)

with open('dictionaryData.pickle', 'wb') as f:
    pickle.dump(datasForPassages, f)

for k, v in datasForPassages.items():
    print(len(v))

df = pd.DataFrame.from_dict(datasForPassages)
print(df)
df.to_excel('results.xlsx')


def GetHapaxForGospel():
    global word
    # Prepare chapter dict
    chapters = {}
    for i in range(1, 22):
        chapter = Chapter()
        chapter.index = i
        chapters[str(i)] = chapter
    for word in GJohnVerseAndLexeme.itertuples():
        chapterCount = word[1].split("｜")[1]

        count = len(GJohnVerseAndLexeme[GJohnVerseAndLexeme['v'] == str(word[3])])
        if count < 2:
            print("Chapter " + str(chapterCount) + word[1] + ": " + word[3] + " is a hapax L, appears: " + str(count))
            chapter = chapters[str(chapterCount)]
            chapter.hapaxes.append(word[3])
            chapters[str(chapterCount)] = chapter
    for chapter in chapters.values():
        print("chapter " + str(chapter.index) + " has HL: " + str(chapter.hapaxes.__len__()) + " examples: ")
        index = 0
        for HL in chapter.hapaxes:
            print(HL)
            index += 1
            if index > 3:
                break



