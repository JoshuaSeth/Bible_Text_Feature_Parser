from string import ascii_letters



def DivisionToBibleBookString(book):
    asList= book.replace("〕", "").replace("〔", "").split("｜")
    string = "JHN "
    string = string + asList[1]+":" +asList[2]
    return string

def ContainsNumber(inputString):
     return any(char.isdigit() for char in inputString)

def DivisionToBCVString(division):
    if not ContainsNumber(division):
        print("WARNING, this division contains no numbers and will be skipped")
        return ""

    if division == "":
        print("WARNING, this division is empty and will be skipped")
        return ""

    if not division.__contains__(":"):
        print("WARNING, this division is incorrectly denoted and will be skipped")
        return ""

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
