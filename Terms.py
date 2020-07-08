lexemes = ['ἀλλά', 'ἐκ', 'μαθητής',
         'ἐγώ', 'εἰμί', 'ἵνα',
          'ἔχω',
         'ἀγαπάω', 'αἰώνιος', 'ἀλήθεια', 'ἀληθής', 'ἀμήν', 'ἀποθνήσκω', 'ἀποκρίνω', 'ἄρτι',
         'γεννάω', 'γινώσκω','δίδωμι', 'δοξάζω', 'ἐγγύς', 'ἐκεῖνος', 'ἐμαυτοῦ', 'ἐμός', 'ἐντολή',
         'ἑορτή', 'ἔργον', 'ἔρχομαι', 'ἐρωτάω', 'ζάω', 'ζητέω', 'ζωή', 'ἤδη', 'θεωρέω', 'ἴδε', 'Ἰησοῦς',
         'ἵνα', 'Ἰουδαῖος', 'κἀγώ', 'καθώς', 'κόσμος', 'κρίνω', 'κρίσις', 'Λάζαρος', 'λαλέω', 'λαμβάνω',
              'μαρτυρέω', 'μαρτυρία', 'μένω', 'μισέω', 'μνημεῖον', 'νίπτω', 'νῦν', 'εἴδω',
         'ὅπου', 'ὁράω', 'ὅτε', 'ὅτι', 'οὐ', 'οὐδείς', 'οὖν', 'οὔπω', 'πάλιν', 'πατήρ', 'πέμπω', 'περιπατέω',
           'Πέτρος', 'Πιλᾶτος', 'πιστεύω', 'πόθεν', 'ποιέω', 'ποῦ', 'πρόβατον', 'προσκυνέω','τηρέω', 'ὕδατος']

#Inccorect
OGNToWords = ['ἀλλὰ', 'ἐκ', 'μαθητής',
         'ἐγώ', 'εἶναι', 'ἤμην', 'ἡμεῖς', 'ἵνα', 'ἔχειν',
         'ἠγάπα', 'αἰώνιος', 'ἀλήθεια', 'ἀληθής', 'ἀμὴν', 'ἀποθνήσκειν', 'ἀποκρίνεται', 'ἄρτι',
         'γεννηθῇ', 'γινώσκω','δίδωμι', 'ἐδοξάσθη', 'ἐγγὺς', 'ἐκεῖνος', 'ἐμαυτοῦ', 'ἐμὸς', 'ἐντολὴ',
         'ἑορτὴ', 'ἔργον', 'ἔρχεσθαι', 'ἐρωτᾶν', 'ζῇ', 'ζητεῖτε', 'ζωή', 'ἤδη', 'θεωρεῖ', 'ἴδε', 'Ἰησοῦς',
         'ἵνα', 'Ἰουδαῖος', 'κἀγὼ', 'καθώς', 'κόσμος', 'κρίνειν', 'κρίσις', 'Λάζαρος', 'λαλεῖν', 'λαμβάνειν',
              'μαρτυρεῖ', 'μαρτυρία', 'μένειν', 'μισεῖν', 'μνημεῖον', 'νίπτειν', 'νῦν', 'οἶδα',
         'ὅπου', 'ὁράω', 'Ὅτε', 'ὅτι', 'οὐ', 'οὐδεὶς', 'οὖν', 'οὔπω', 'πάλιν', 'πατήρ', 'πέμπω', 'περιπατέω',
              'Πέτρος', 'Πιλᾶτος', 'πιστεύω', 'πόθεν', 'ποιέω', 'ποῦ', 'πρόβατον', 'προσκυνέω', 'τηρέω', 'ὕδωρ']

prepositions = ['ἐν', 'παρά', 'περί', 'πρό', 'ἀπό', 'ἐπί', 'κατά', 'ἐκ', 'εἰς']

deounlist = ['οὖν', 'δέ']

otherList = ['αὐτού', 'αὐτὀς', 'αὐτῷ', 'εἰ', 'εἰ μὴ', 'τοῦτο', 'τούτου', 'τούτῳ', 'τοῦτον', 'ταῦτα', 'ἐάν', 'ἐάν μὴ', 'ὅς']

#γεννᾶν is not found anywhere in NT probasbly should be γεννηθῇ? Or another form of GEnnaoo? but Morgenthaler has the former
#None of the syllables of γιδόναι can i find in GJhon Morgenthaler reports 76: γίνομαι?
#ζετεῖν not found anywhere in gospel replaced with ζητέite
#ζῆν can't found out this one ζάω replaced it but only found 3 times according to MThaler should be found 17 in GJOHN
#μαρτυρεῖv without closing n
#ἐδοξάσθη case of doubt ἑορτὴ ook
#Oran = ὁράω? CANT FIND
#Found but is this correct in Berean bible??
#ἠγάπαv is ἠγάπα?
#ὰποχρίνεσθαι is Ἀπεκρίθη?
# is ἡμεῖς?
#ἀμὴν has also version with Capital should check if this one is found
# ἐντολὴ van OGNTo Morgenthaler has stripe pointing wrong direction
#ὰποκρίνεσθαι cannot find OGNTo, replaced with ἀποκρίνεται
# οὐδεὶς replaced as οὐδεὶς bij OGNTo this is not how morgenthaler spells it
#theorien in Morgenthaler replaced with θεωρεῖ
#DZetein replaced with ζητεῖτε but there wqere more possible variants of Zeteoo which only diverged for one or two characters
#Agapan = ἀγαπάω?
#When seeing gidonai as didomi it fits
#Oida komt op Eido uit maar is 85 vs 120
# Pempein = πέμπω
#Peripatein = περιπατέω
# Pisteuein = πιστεύω
# Poiein = ποιέω
# Proskunein = προσκυνέω
# Terein = τηρέω
# Udoor = ὕδωρ = ὕδατος

print(len(OGNToWords))