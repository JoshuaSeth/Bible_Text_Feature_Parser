import BibleToDF as btf
import Terms as t
import Morphology as m

NT = btf.GetALLNTLexemes()

relpro = 0
corpro = 0
doubtcorpro = 0
total = 0
refused = 0
refusedButNotCompound = 0

for row in NT.itertuples():
    OGNToWord = row[4]

    if t.relativePronounForms.__contains__(OGNToWord):
        Gcode = row[6]
        if not m.dictionary[Gcode].__contains__("pronoun"):
            if not m.dictionary[Gcode].__contains__("Relative") and not m.dictionary[Gcode].__contains__("Correlative"):
                refused+=1
                if Gcode != "G3754":
                    refusedButNotCompound+=1

    if m.dictionary[row[6]].__contains__("pronoun"):
        if m.dictionary[row[6]].__contains__("Relative"):
            relpro+=1
            total+=1
        if m.dictionary[row[6]].__contains__("correlative"):
            corpro+=1
            total+=1
            if m.dictionary[row[6]].__contains__("or"):
                doubtcorpro+=1

print("Relpro: "+str(relpro) )
print("Corpro: "+str(corpro) )
print("of which doubtful: " + str(doubtcorpro))
print("Total: "+str(total) )
print("Refused: "+str(refused) )
print("Refused but not compound: "+str(refusedButNotCompound) )
print("Total should be 1680")