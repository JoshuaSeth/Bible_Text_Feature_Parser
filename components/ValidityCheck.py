import pandas as pd
import Terms as t


def CheckValidity(inputExcel):
    """Checks if results are valid or if some columns only contain 0 values"""
    df = pd.read_excel(inputExcel)
    with open("Validity Check Results.txt", "w") as textFile:
        textFile.write("VALIDITY CHECK RESULTS" + "\n")
    for columnName, column in df.iteritems():
        if not columnName.__contains__("ratio"):
            if(column == 0).all():
                with open("Validity Check Results.txt", "a") as textFile:
                    textFile.write(columnName+ " contains only zeros"+"\n")
            with open("Validity Check Results.txt", "a") as textFile:
                textFile.write(columnName + " total: " + str(df[columnName].sum()) +"\n")



    print("Lexemes are a total of: "+ str(len(t.lexemes))+". Should be less than " + str(len(t.OGNToWords)) + ".")
    print("OGNTO words are a total of: " + str(len(t.OGNToWords)) + ". Should be 75.")



CheckValidity("results.xlsx")