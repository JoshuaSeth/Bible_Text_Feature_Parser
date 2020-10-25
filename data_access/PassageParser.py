from string import ascii_letters
import warnings



def DivisionToBibleBookString(book):
    asList= book.replace("〕", "").replace("〔", "").split("｜")
    string = "JHN "
    string = string + asList[1]+":" +asList[2]
    return string

def ContainsNumber(inputString):
     return any(char.isdigit() for char in inputString)

def DivisionToBCVStringList(division):
    BCVStringList = []
    if not ContainsNumber(division):
        warnings.warn("WARNING, this division contains no numbers and will be skipped: " +str(division))
        return ""

    if division == "":
        warnings.warn("WARNING, this division is empty and will be skipped: " +str(division))
        return ""

    if not division.__contains__(":" or ","):
        warnings.warn("WARNING, this division is incorrectly denoted and will be skipped: " +str(division))
        return""

    #Some preprocessing
    division = str(division)
    division =division.replace(")", "")
    division =division.replace("(", "")

    #Check if it is one or multiple divisions
    if division.__contains__("&"):
        twoDivisions = division.split("&")
        Parse(BCVStringList, twoDivisions[0])
        Parse(BCVStringList, twoDivisions[1])
    else:
        Parse(BCVStringList, division)

    print(str(division) + " parsed to: " + str(BCVStringList))

    return BCVStringList


def Parse(BCVStringList, division):
    # Remove any alphabetic letters
    division = ''.join(c for c in division if c not in ascii_letters)
    # Create a list for string keys to find in the bible.csvs
    # Check if it spans multiple chapter or only one
    splitDivision = division.split(":")
    chapter = splitDivision[0]
    verses = splitDivision[1].split("-")
    for chapterNr in range(int(verses[0]), int(verses[1]) + 1):
        BCVStringList.append("〔43｜" + chapter + "｜" + str(chapterNr) + "〕")
    return BCVStringList




