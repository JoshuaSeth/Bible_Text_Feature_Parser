import pandas as pd
import PassageParser as pp
import MarkupReader as mur
import Strongs
import Terms as t
import CompoundWords as cw
import Morphology as m

def GetFeaturesForPassage(passage, onlyCountWords, GJohnVerseAndLexeme, useLexemesForPTTerms=False, NT=None, excludeForHLCount=None):
    #Check if it is a valid sequence
    print("Sequence: " + str(passage))
    if pd.isna(passage):
        print("Error, a NAN found, skipping this sequence")
        return None

    isPA = False
    if passage == "7:53-53&8:1-11":
        isPA=True
    parsedSequence = pp.DivisionToBCVStringList(passage)

    if parsedSequence == "":
        print("Warning, an empty sequence returned from parser, skipping this sequence")
        return None


    #Count Propositions, preference terms and, de/oun ratios
    #Johaninne Preference Words
    ptCount = {}
    if (not onlyCountWords):
        ptCount["Total"] =0
        if useLexemesForPTTerms:
            for term in t.lexemes:
                ptCount[term] = 0
        else:
            for term in t.OGNToWords:
                ptCount[term] = 0

    #Prepositions
    prpCount = {}
    if (not onlyCountWords):
        prpCount["Total"]=0
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
    featureCount["Hapaxes in GJohn Lemma"] = []
    featureCount["Hapaxes in GJohn OGNT"] = []
    if NT is not None:
        featureCount["Hapax Legomena Lemma NT"] = 0
        featureCount['Hapax Legomena OGNTo Word NT'] = 0
        featureCount["Hapaxes in NT Lemma"] = []
        featureCount["Hapaxes in NT OGNT"] = []
    featureCount["Compound Words"] = 0
    featureCount["Foreign Words"] = 0
    featureCount["Historical Present"] = 0
    featureCount["Relative Pronouns"] = 0

    sequenceTotalWords = 0

    errorData = {}
    errorData["Refused pronouns"]=[]
    errorData["GCodes of refused"]=[]
    errorData["Unrecognized relative forms"]=[]


    for verseTag in parsedSequence:
        #Select all rows from df which are part of this verse
        rowsForVerse = GJohnVerseAndLexeme.loc[GJohnVerseAndLexeme['〔Book｜Chapter｜Verse〕'] == verseTag]
        sequenceTotalWords += len(rowsForVerse)

        if(not onlyCountWords):
            #Historical presents are counted for the whole verse so not per word row of the verse
            featureCount['Historical Present'] += mur.MarkUpContainsHistoricalPresent(
                pp.DivisionToBibleBookString(verseTag))

            for wordRow in rowsForVerse.itertuples():

                #Count 4 Hapax Legomena versions

                lexeme = wordRow[3]
                OGNToWord = wordRow[4]
                # John
                lemmaCountInGJohn = len(GJohnVerseAndLexeme[GJohnVerseAndLexeme['v'] == str(lexeme)]) - len(excludeForHLCount[excludeForHLCount['v'] == str(lexeme)])

                #if this is not the passge of the word is found only once it is HL, is this is the passge the passage count is subtracted fomr total count so 0 should be found
                maxToBeFound =1
                if not isPA:
                    maxToBeFound+=1

                if lemmaCountInGJohn < maxToBeFound and not featureCount["Hapaxes in GJohn Lemma"].__contains__(str(lexeme)):
                    featureCount['Hapax Legomena Lemma']+=1
                    featureCount["Hapaxes in GJohn Lemma"].append(str(lexeme))
                wordCountInGJohn = len(GJohnVerseAndLexeme[GJohnVerseAndLexeme['ognto'] == str(OGNToWord)]) - len(excludeForHLCount[excludeForHLCount['ognto'] == str(OGNToWord)])
                if wordCountInGJohn < maxToBeFound and not featureCount["Hapaxes in GJohn OGNT"].__contains__(str(OGNToWord)):
                    featureCount['Hapax Legomena OGNTo Word'] += 1
                    featureCount["Hapaxes in GJohn OGNT"].append(str(OGNToWord))

                #Whole NT
                if NT is not None:
                    lemmaCountinNT = len(NT[NT['v'] == str(lexeme)]) - len(excludeForHLCount[excludeForHLCount['v'] == str(lexeme)])
                    if lemmaCountinNT < maxToBeFound and not featureCount["Hapaxes in NT Lemma"].__contains__(str(lexeme)):
                        featureCount['Hapax Legomena Lemma NT'] += 1
                        featureCount["Hapaxes in NT Lemma"].append(str(lexeme))
                    wordCountInNT = len(NT[NT['ognto'] == str(OGNToWord)]) - len(excludeForHLCount[excludeForHLCount['ognto'] == str(OGNToWord)])
                    if wordCountInNT < maxToBeFound and not featureCount["Hapaxes in NT OGNT"].__contains__(str(OGNToWord)):
                        featureCount['Hapax Legomena OGNTo Word NT'] += 1
                        featureCount["Hapaxes in NT OGNT"].append(str(OGNToWord))

                if cw.compoundList.__contains__(lexeme):
                    featureCount['Compound Words']+=1
                    print(lexeme + " is a compound")
                if Strongs.foreignWords.__contains__(lexeme):
                    if(not lexeme.__contains__('Ἰησοῦς')):
                        featureCount['Foreign Words']+=1
                        print(lexeme + " is a foreign word")

                if useLexemesForPTTerms:
                    if ptCount.__contains__(lexeme):
                        ptCount[lexeme]+=1
                        ptCount["Total"] +=1
                if not useLexemesForPTTerms:
                    if ptCount.__contains__(OGNToWord):
                        ptCount[OGNToWord]+=1
                        ptCount["Total"] += 1
                if prpCount.__contains__(lexeme):
                    prpCount[lexeme]+=1
                    prpCount["Total"] += 1
                if deounCount.__contains__(lexeme):
                    deounCount[lexeme]+=1

                if t.relativePronounForms.__contains__(OGNToWord):
                    Gcode = wordRow[6]
                    if not m.dictionary[Gcode].__contains__("pronoun"):
                        if not m.dictionary[Gcode].__contains__("Relative") and not m.dictionary[Gcode].__contains__("Correlative"):
                            errorData["Refused pronouns"].append(OGNToWord)
                            errorData["GCodes of refused"].append(Gcode)

                if m.dictionary[wordRow[6]].__contains__("pronoun"):
                    if m.dictionary[wordRow[6]].__contains__("Relative") or m.dictionary[wordRow[6]].__contains__("Correlative"):
                        featureCount["Relative Pronouns"] += 1
                        if not t.relativePronounForms.__contains__(OGNToWord):
                            errorData["Unrecognized relative forms"].append(OGNToWord)

    metadata = {}
    metadata['Passage'] = passage
    metadata['Word Count'] = sequenceTotalWords


    return [metadata, featureCount, deounCount ,prpCount, ptCount, errorData]




def ReadFeaturesForColumn(verseDivisionList, datasForPassages, OnlyWordCount, GJohnVerseAndLexeme, UseLexemesForPTCount=False, NT=None, excludeForHLCount=None, calculateRatios=False):
    for sequence in verseDivisionList:
        data = GetFeaturesForPassage(sequence, onlyCountWords=OnlyWordCount, GJohnVerseAndLexeme=GJohnVerseAndLexeme, useLexemesForPTTerms=UseLexemesForPTCount, NT=NT, excludeForHLCount=excludeForHLCount)
        if data is not None:
            wordCount = data[0]["Word Count"]
            print(wordCount)
            dictInd = 0
            for dictionary in data:
                dictInd += 1
                for dataPointKey, dataPointVal in dictionary.items():
                    newKey = str(dictInd) + ": " + str(dataPointKey)
                    if calculateRatios:
                        ratioKey = str(dictInd) + ": " + str(dataPointKey) + " ratio"
                    if not datasForPassages.__contains__(newKey):
                        datasForPassages[newKey] = []
                    datasForPassages[newKey].append(dataPointVal)

                    # Ratio's
                    if calculateRatios:
                        if isinstance(dataPointVal, int):
                            if not datasForPassages.__contains__(ratioKey):
                                datasForPassages[ratioKey] = []
                            if dataPointVal != 0 and wordCount != 0:
                                datasForPassages[ratioKey].append(dataPointVal / wordCount)
                            else:
                                datasForPassages[ratioKey].append(0)
        print(data)