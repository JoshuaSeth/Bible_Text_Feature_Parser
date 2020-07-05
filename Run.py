import pandas as pd
import pickle


import BibleToDF as btf
GJohnVerseAndLexeme =  btf.GetLexemesForBibleBook(43, True)


datasForPassages = {}

import FeatureScanner as fp

OnlyWordCount = False
ForeachColumn = False

excelWithSequences = pd.read_excel('Outline John.xlsx')
verseDivisionList = excelWithSequences["Morris"]


if(ForeachColumn):
    # creating a list of dataframe columns
    columns = list(excelWithSequences)

    for i in columns:
        fp.ReadFeaturesForColumn(i, datasForPassages, OnlyWordCount,GJohnVerseAndLexeme)

if not ForeachColumn:
    fp.ReadFeaturesForColumn(verseDivisionList, datasForPassages, OnlyWordCount,GJohnVerseAndLexeme)


with open('dictionaryData.pickle', 'wb') as f:
    pickle.dump(datasForPassages, f)

for k, v in datasForPassages.items():
    print(len(v))

df = pd.DataFrame.from_dict(datasForPassages)
print(df)
df.to_excel('results.xlsx')




