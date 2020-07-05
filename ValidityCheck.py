import pandas as pd


def CheckValidity(inputExcel):
    """Checks if results are valid or if some columns only contain 0 values"""
    df = pd.read_excel(inputExcel)
    with open("Validity Check Results.txt", "w") as textFile:
        textFile.write("VALIDITY CHECK RESULTS" + "\n" + "Only zero's found for columns:" + "\n")
    for columnName, column in df.iteritems():
        if(column == 0).all():
            print(columnName + " contains only zeros")
            with open("Validity Check Results.txt", "a") as textFile:
                textFile.write(columnName+"\n")



CheckValidity("results.xlsx")