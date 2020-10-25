import pandas as pd
import pickle

#This is the top level script to run all other things

import BibleToDF as btf

pericope = btf.GetLexemesForDivision("7:53-53&8:1-11")
GJohnVerseAndLexeme =  btf.GetLexemesForBibleBook(43)
NewTestament = btf.GetALLNTLexemes()


import FeatureScanner as fp


excelWithSequences = pd.read_excel('Nieuwe indeling Outlier test.xlsx')
verseDivisionList = excelWithSequences["Corrected"]

datasForPassages = {}
fp.ReadFeaturesForColumn(verseDivisionList, datasForPassages, False, GJohnVerseAndLexeme, True, None, pericope)

with open('dictionaryData.pickle', 'wb') as f:
    pickle.dump(datasForPassages, f)

for k, v in datasForPassages.items():
    print(len(v))

df = pd.DataFrame.from_dict(datasForPassages)
print(df)
df.to_excel('resultsWithLuke.xlsx')
