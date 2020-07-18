#When you have a stem, when this stem is also part of another word, this other word probably is a compound
import Terms as t
compoundList = []
compoundHashes = set()

def CreateCompoundList(bibleDF):
    print("Start creation of compound list")
    with open("Compound words.txt", "w") as textFile:
        textFile.write("Compound words: " + "\n")
    textFile.close()

    count = 0
    currentString = ""
    for wordRow in bibleDF.itertuples():
        count+=1
        lemma  = wordRow[3][1:]
        if lemma=="":
            continue
        code = wordRow[5]
        if code[0] == "V" or code[0] == "N":
            for wordRow2 in bibleDF.itertuples():
                possibleCompound = wordRow2[3]
                code = wordRow2[5]
                if code[0] == "V" or code[0] == "N":
                    if not possibleCompound == lemma:
                        if possibleCompound.__contains__(lemma):
                            if (len(possibleCompound.split(lemma)) == 2):
                                if not compoundHashes.__contains__(possibleCompound):

                                    add = False
                                    for prepositionForm in t.allPrepositionForms:
                                        if possibleCompound.__contains__(prepositionForm):
                                            add = True
                                            break
                                    if add:
                                        currentString += possibleCompound+ "\n"
                                        compoundList.append(possibleCompound)
                                        compoundHashes.add(possibleCompound)
                                        print(possibleCompound + " row " + str(count) + " of " + str(bibleDF.shape[0]))

        if count%20 == 0:
            with open("Compound words.txt", "a") as textFile:
                textFile.write(currentString)
                currentString=""
            textFile.close()


with open("Compound words in John.txt", "r") as textFile:
    string = textFile.read()
    compoundList = string.split("\n")

# import BibleToDF as btf
# bibleData = btf.GetALLNTLexemes()
# CreateCompoundList(bibleData)

