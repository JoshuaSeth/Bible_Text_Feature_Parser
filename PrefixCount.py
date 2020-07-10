#COunting prefixes to test validity of compound words
import re

#From Eliran Wong
searchReplace = (
    ('[ἀἄᾄἂἆἁἅᾅἃάᾴὰᾶᾷᾳ]', 'α'),
    ('[ἈἌἎἉἍἋ]', 'Α'),
    ('[ἐἔἑἕἓέὲ]', 'ε'),
    ('[ἘἜἙἝἛ]', 'Ε'),
    ('[ἠἤᾔἢἦᾖᾐἡἥἣἧᾗᾑήῄὴῆῇῃ]', 'η'),
    ('[ἨἬἪἮἩἭἫ]', 'Η'),
    ('[ἰἴἶἱἵἳἷίὶῖϊΐῒ]', 'ι'),
    ('[ἸἼἹἽ]', 'Ι'),
    ('[ὀὄὂὁὅὃόὸ]', 'ο'),
    ('[ὈὌὉὍὋ]', 'Ο'),
    ('[ῥ]', 'ρ'),
    ('[Ῥ]', 'Ρ'),
    ('[ὐὔὒὖὑὕὓὗύὺῦϋΰῢ]', 'υ'),
    ('[ὙὝὟ]', 'Υ'),
    ('[ὠὤὢὦᾠὡὥὧᾧώῴὼῶῷῳ]', 'ω'),
    ('[ὨὬὪὮὩὭὯ]', 'Ω'),
    ("[\-\—\,\;\:\\\?\.\·\·\'\‘\’\‹\›\“\”\«\»\(\)\[\]\{\}\⧼\⧽\〈\〉\*\‿\᾽\⇔\¦]", ""),
)

#prefixList = ["συν", 'συλ','συμ','συγ', 'συ']
prefixList = ["κατ"]


hapaxesInPA = ['ἐλαιών', 'ὄρθρος', 'γραμματεύς', 'μοιχεία', 'ἐπαυτόφωρος, αὐτόφωρος', 'μοιχεύω', 'κύπτω', 'καταγράφω', 'ἐπιμένω', 'ἀνακύπτω', 'ἀναμάρτητος', 'κατακύπτω', 'πρεσβύτερος', 'καταλείπω', 'κατακρίνω']

import BibleToDF as btf


def Test(nr):
    alreadyFound = []
    prefixCount = 0
    GJohn = btf.GetLexemesForBibleBook(nr)
    for row in GJohn.itertuples():
        word = row[3]
        for search, replace in searchReplace:
            word = re.sub(search, replace, word)
        for prefix in prefixList:
            if word.__contains__(prefix) and not word == prefix and not alreadyFound.__contains__(word) and word.split(prefix)[0] == "" and word != prefix+"ω":
                if word.endswith("ω") or word.endswith("μαι")or word.endswith("ναι"):
                    if hapaxesInPA.__contains__(row[3]) and nr == 43:
                        continue
                    prefixCount += 1
                    alreadyFound.append(word)
                    print(word)
    return prefixCount

def Test2(nr):
    import CompoundWords as cw
    alreadyFound = []
    prefixCount = 0
    GJohn = btf.GetLexemesForBibleBook(nr)
    for row in GJohn.itertuples():
        word = row[3]
        # for search, replace in searchReplace:
        #     word = re.sub(search, replace, word)
        if cw.compoundList.__contains__(word):
            if not alreadyFound.__contains__(word):
                prefixCount += 1
                alreadyFound.append(word)
    return prefixCount

print(Test2(43))


prefixCount = Test(40)
print(prefixCount)
prefixCount = Test(41)
print(prefixCount)
prefixCount = Test(42)
print(prefixCount)
prefixCount = Test(43)
print(prefixCount)

#5, 10, 17, 7