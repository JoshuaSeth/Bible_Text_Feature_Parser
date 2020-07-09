import pandas as pd
import PassageParser as pp
import MarkupReader as mur
import Strongs
import Terms as t

def GetFeaturesForPassage(passage, onlyCountWords, GJohnVerseAndLexeme, useLexemes=False):
    #Check if it is a valid sequence
    print("Sequence: " + str(passage))
    if pd.isna(passage):
        print("Error, a NAN found, skipping this sequence")
        return None

    parsedSequence = pp.DivisionToBCVStringList(passage)

    if parsedSequence == "":
        print("Warning, an empty sequence returned from parser, skipping this sequence")
        return None


    #Count Propositions, preference terms and, de/oun ratios
    #Johaninne Preference Words
    ptCount = {}
    if (not onlyCountWords):
        if useLexemes:
            for term in t.lexemes:
                ptCount[term] = 0
        else:
            for term in t.OGNToWords:
                ptCount[term] = 0

    #Propositions
    prpCount = {}
    if (not onlyCountWords):
        for term in t.prepositions:
            prpCount[term] = 0

    #De/Oun
    deounCount = {}
    if (not onlyCountWords):
        for term in t.deounlist:
            deounCount[term] = 0

    featureCount = {}
    featureCount["Hapax Legomena Lemma"] = 0
    featureCount['Hapax Legomena OGNTo Word'] = 0
    featureCount["Compound Words"] = 0
    featureCount["Foreign Words"] = 0
    featureCount["Historical Present"] = 0

    sequenceTotalWords = 0



    for verseTag in parsedSequence:
        #Select all rows from df which are part of this verse
        rowsForVerse = GJohnVerseAndLexeme.loc[GJohnVerseAndLexeme['〔Book｜Chapter｜Verse〕'] == verseTag]
        sequenceTotalWords += len(rowsForVerse)

        if(not onlyCountWords):
            #Historical presents are counted for the whole verse so not per word row of the verse
            featureCount['Historical Present'] += mur.MarkUpContainsHistoricalPresent(
                pp.DivisionToBibleBookString(verseTag))

            for wordRow in rowsForVerse.itertuples():
                lexeme = wordRow[3]
                OGNToWord = wordRow[4]
                lemmaCountInGJohn = len(GJohnVerseAndLexeme[GJohnVerseAndLexeme['v'] == str(lexeme)])
                if lemmaCountInGJohn < 2:
                    featureCount['Hapax Legomena Lemma']+=1

                wordCountInGJohn = len(GJohnVerseAndLexeme[GJohnVerseAndLexeme['ognto'] == str(OGNToWord)])
                if wordCountInGJohn < 2:
                    featureCount['Hapax Legomena OGNTo Word'] += 1

                if Strongs.compoundWords.__contains__(lexeme):
                    featureCount['Compound Words']+=1
                    print(lexeme + " is a compound")
                if Strongs.foreignWords.__contains__(lexeme):
                    if(not lexeme.__contains__('Ἰησοῦς')):
                        featureCount['Foreign Words']+=1
                        print(lexeme + " is a foreign word")

                if useLexemes:
                    if ptCount.__contains__(lexeme):
                        ptCount[lexeme]+=1
                if not useLexemes:
                    if ptCount.__contains__(OGNToWord):
                        ptCount[OGNToWord]+=1
                if prpCount.__contains__(lexeme):
                    prpCount[lexeme]+=1
                if deounCount.__contains__(lexeme):
                    deounCount[lexeme]+=1

    metadata = {}
    metadata['Passage'] = passage
    metadata['Word Count'] = sequenceTotalWords


    return [metadata, featureCount, deounCount ,prpCount, ptCount]




def ReadFeaturesForColumn(verseDivisionList, datasForPassages, OnlyWordCount, GJohnVerseAndLexeme, UseLexemes=False):
    for sequence in verseDivisionList:
        data = GetFeaturesForPassage(sequence, onlyCountWords=OnlyWordCount, GJohnVerseAndLexeme=GJohnVerseAndLexeme, useLexemes=UseLexemes)
        if data is not None:
            wordCount = data[0]["Word Count"]
            print(wordCount)
            dictInd = 0
            for dictionary in data:
                dictInd += 1
                for dataPointKey, dataPointVal in dictionary.items():
                    newKey = str(dictInd) + ": " + str(dataPointKey)
                    ratioKey = str(dictInd) + ": " + str(dataPointKey) + " ratio"
                    if not datasForPassages.__contains__(newKey):
                        datasForPassages[newKey] = []
                    datasForPassages[newKey].append(dataPointVal)

                    # Ratio's
                    if isinstance(dataPointVal, int):
                        if not datasForPassages.__contains__(ratioKey):
                            datasForPassages[ratioKey] = []
                        if dataPointVal != 0 and wordCount != 0:
                            datasForPassages[ratioKey].append(dataPointVal / wordCount)
                        else:
                            datasForPassages[ratioKey].append(0)
        print(data)