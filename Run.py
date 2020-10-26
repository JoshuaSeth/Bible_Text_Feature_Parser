# This is the top level script to run all other things

from data_access import Bible as b

John = b.GetBookDF(42)

print(John)



# datasForPassages = {}
# fp.ReadFeaturesForColumn(verseDivisionList, datasForPassages,
#                          False, GJohnVerseAndLexeme, True, None, pericope)

# with open('dictionaryData.pickle', 'wb') as f:
#     pickle.dump(datasForPassages, f)

# for k, v in datasForPassages.items():
#     print(len(v))

# df = pd.DataFrame.from_dict(datasForPassages)
# print(df)
# df.to_excel('resultsWithLuke.xlsx')
