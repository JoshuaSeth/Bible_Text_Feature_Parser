lexemes = ['ἀλλά', 'ἐκ', 'μαθητής',
         'ἐγώ', 'εἰμί', 'ἵνα',
         'οὗτος', 'ἔχω',
         'ἀγαπάω', 'αἰώνιος', 'ἀλήθεια', 'ἀληθής', 'ἀμήν', 'ἀποθνήσκω', 'ἀποκρίνω', 'ἄρτι',
         'γεννάω', 'γινώσκω', 'δοξάζω', 'ἐγγύς', 'ἐκεῖνος', 'ἐμαυτοῦ', 'ἐμός', 'ἐντολή',
         'ἑορτή', 'ἔργον', 'ἔρχομαι', 'ἐρωτάω', 'ζάω', 'ζητέω', 'ζωή', 'ἤδη', 'θεωρέω', 'ἴδε', 'Ἰησοῦς',
         'ἵνα', 'Ἰουδαῖος', 'κἀγώ', 'καθώς', 'κόσμος', 'κρίνω', 'κρίσις', 'Λάζαρος', 'λαλέω', 'λαμβάνω',
              'μαρτυρέω', 'μαρτυρία', 'μένω', 'μισέω', 'μνημεῖον', 'νίπτω', 'νῦν', 'εἴδω',
         'ὅπου', 'ὁράω', 'ὅτε', 'ὅτι', 'οὐ','σύ', 'οὐδείς', 'οὖν', 'οὔπω']

#Inccorect
OGNToWords = ['ἀλλὰ', 'ἐκ', 'μαθητής',
         'ἐγώ', 'εἶναι', 'ἤμην', 'ἡμεῖς', 'ἵνα',
         'οὗτος', 'ἔχειν',
         'ἠγάπα', 'αἰώνιος', 'ἀλήθεια', 'ἀληθής', 'ἀμὴν', 'ἀποθνήσκειν', 'ἀποκρίνεται', 'ἄρτι',
         'γεννηθῇ', 'γινώσκω', 'ἐδοξάσθη', 'ἐγγὺς', 'ἐκεῖνος', 'ἐμαυτοῦ', 'ἐμὸς', 'ἐντολὴ',
         'ἑορτὴ', 'ἔργον', 'ἔρχεσθαι', 'ἐρωτᾶν', 'ζῇ', 'ζητεῖτε', 'ζωή', 'ἤδη', 'θεωρεῖ', 'ἴδε', 'Ἰησοῦς',
         'ἵνα', 'Ἰουδαῖος', 'κἀγὼ', 'καθώς', 'κόσμος', 'κρίνειν', 'κρίσις', 'Λάζαρος', 'λαλεῖν', 'λαμβάνειν',
              'μαρτυρεῖ', 'μαρτυρία', 'μένειν', 'μισεῖν', 'μνημεῖον', 'νίπτειν', 'νῦν', 'οἶδα',
         'ὅπου', 'ὁράω', 'Ὅτε', 'ὅτι', 'οὐ','σύ', 'οὐδεὶς', 'οὖν', 'οὔπω']

prepositions = ['ἐν', 'παρά', 'περί', 'πρό', 'ἀπό', 'ἐπί', 'κατά', 'ἐκ', 'εἰς']

deounlist = ['οὖν', 'δέ']

otherList = ['αὐτού', 'αὐτὀς', 'αὐτῷ', 'εἰ', 'εἰ μὴ', 'τοῦτο', 'τούτου', 'τούτῳ', 'τοῦτον', 'ταῦτα', 'ἐάν', 'ἐάν μὴ', 'ὅς']

#γεννᾶν is not found anywhere in NT probasbly should be γεννηθῇ? Or another form of GEnnaoo? but Morgenthaler has the former
#None of the syllables of γιδόναι can i find in GJhon Morgenthaler reports 76: γίνομαι?
#ζετεῖν not found anywhere in gospel replaced with ζητέite
#ζῆν can't found out this one ζάω replaced it but only found 3 times according to MThaler should be found 17 in GJOHN
#μαρτυρεῖv zonder slot n
#ἐδοξάσθη case of doubt ἑορτὴ ook
#Oran = ὁράω? CANT FIND
#Found but is this correct in Berean bible??
#ἠγάπαv is ἠγάπα?
#ὰποχρίνεσθαι is Ἀπεκρίθη?
# is ἡμεῖς?
#ἀμὴν has also version with Capital should check if this one is found
# ἐντολὴ van OGNTo Morgenthaler has stripe pointing wrong direction
#ὰποκρίνεσθαι  is absoluut onvindbaar in OGNTo, vervangen door ἀποκρίνεται
# οὐδεὶς vervangen als οὐδεὶς bij OGNTo ookal staat het niet zo bij Morgenthaler
#theorien bij MGT vervangen door θεωρεῖ
#DZetein vervangen door ζητεῖτε maar er waren nog meer varianten van Zeteoo die maar één letter afwijkten

print(len(OGNToWords))