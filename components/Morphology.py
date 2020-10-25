dictionary = {}

def ReadDictionary():
    import pandas as pd
    dict = pd.read_csv("OpenGNT_morphology_English.csv", sep='	')

    for row in dict.itertuples():
        dictionary[row[2]] = row[4].split(",")[0]

ReadDictionary()