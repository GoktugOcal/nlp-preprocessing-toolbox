# from nlp_preprocessing_toolbox.helper import *

import re

class Suffix(object):
    def __init__(self, name, pattern, optionalLetter, checkHarmony):
        self.name = name
        self.pattern = re.compile("(" + pattern + ")$", re.UNICODE)

        if optionalLetter is None:
            self.optionalLetterCheck = False
            self._optionalLetterPattern = None
        else:
            self.optionalLetterCheck = True
            self._optionalLetterPattern = re.compile("(" + optionalLetter + ")$", re.UNICODE)

        self.checkHarmony = checkHarmony

    def Match(self, word):
        return self.pattern.search(word)

    def OptionalLetter(self, word):
        if self.optionalLetterCheck:
            match = self._optionalLetterPattern.search(word)
            if match:
                return match.group()

    def RemoveSuffix(self, word):
        return self.pattern.sub("", word)

    @property
    def CheckHarmony(self):
        return self.checkHarmony


#############################################

S1 = Suffix("-lU", "lı|li|lu|lü", None, True)

DERIVATIONAL_SUFFIXES = (S1, )

#############################################



S11 = Suffix("-cAsInA",    "casına|çasına|cesine|çesine",      None, True)
S4  = Suffix("-sUnUz",     "sınız|siniz|sunuz|sünüz",          None, True)
S14 = Suffix("-(y)mUş",    "muş|miş|müş|mış",                  "y",  True)
S15 = Suffix("-(y)ken",    "ken",                              "y",  True)
S2  = Suffix("-sUn",       "sın|sin|sun|sün",                  None, True)
S5  = Suffix("-lAr",       "lar|ler",                          None, True)
S9  = Suffix("-nUz",       "nız|niz|nuz|nüz",                  None, True)
S10 = Suffix("-DUr",       "tır|tir|tur|tür|dır|dir|dur|dür",  None, True)
S3  = Suffix("-(y)Uz",     "ız|iz|uz|üz",                      "y",  True)
S1  = Suffix("-(y)Um",     "ım|im|um|üm",                      "y",  True)
S12 = Suffix("-(y)DU",     "dı|di|du|dü|tı|ti|tu|tü",          "y",  True)
S13 = Suffix("-(y)sA",     "sa|se",                            "y",  True)
S6  = Suffix("-m",         "m",                                None, True)
S7  = Suffix("-n",         "n",                                None, True)
S8  = Suffix("-k",         "k",                                None, True)

# The order of the enum definition determines the priority of the suffix.
# For example, -(y)ken (S15 suffix) is  checked before -n (S7 suffix).
NOMINAL_VERB_SUFFIXES = (S11,S4,S14,S15,S2,S5,S9,S10,S3,S1,S12,S13,S6,S7,S8)



#############################################


S16 = Suffix("-nDAn",     "ndan|ntan|nden|nten",      None,       True)
S7  = Suffix("-lArI",     "ları|leri",                None,       True)
S3  = Suffix("-(U)mUz",   "mız|miz|muz|müz",          "ı|i|u|ü",  True) 
S5  = Suffix("-(U)nUz",   "nız|niz|nuz|nüz",          "ı|i|u|ü",  True) 
S1  = Suffix("-lAr",      "lar|ler",                  None,       True)
S14 = Suffix("-nDA",      "nta|nte|nda|nde",          None,       True)
S15 = Suffix("-DAn",      "dan|tan|den|ten",          None,       True)
S17 = Suffix("-(y)lA",    "la|le",                    "y",        True)
S10 = Suffix("-(n)Un",    "ın|in|un|ün",              "n",        True)
S19 = Suffix("-(n)cA",    "ca|ce",                    "n",        True)
S4  = Suffix("-Un",       "ın|in|un|ün",              None,       True)
S9  = Suffix("-nU",       "nı|ni|nu|nü",              None,       True) 
S12 = Suffix("-nA",       "na|ne",                    None,       True)
S13 = Suffix("-DA",       "da|de|ta|te",              None,       True)
S18 = Suffix("-ki",       "ki",                       None,       False)
S2  = Suffix("-(U)m",     "m",                        "ı|i|u|ü",  True)
S6  = Suffix("-(s)U",     "ı|i|u|ü",                  "s",        True)
S8  = Suffix("-(y)U",     "ı|i|u|ü",                  "y",        True)
S11 = Suffix("-(y)A",     "a|e",                      "y",        True)

# The order of the enum definition determines the priority of the suffix.
# For example, -(y)ken (S15 suffix) is  checked before -n (S7 suffix).
NOUN_SUFFIXES = (S16,S7,S3,S5,S1,S14,S15,S17,S10,S19,S4,S9,S12,S13,S18,S2,S6,S8,S11)

#############################################



class State:
    def __init__(self, word, suffix, nextState = None):
        self.word = word
        self.suffix = suffix
        self.nextState = nextState

words = ["hayran"]
suffixes = []
for word in words:
    for suff_type in [DERIVATIONAL_SUFFIXES, NOMINAL_VERB_SUFFIXES, NOUN_SUFFIXES]:
        for suff in suff_type:
            match = suff.Match(word)
            if match != None:
                print(suff.name)
                suffixes.append((match.group(), match.span()))
                word = suff.RemoveSuffix(word)
                words.append(word)

suffixes = sorted(suffixes, key=lambda x: x[1][0])
print([word] + suffixes)



# 0- o
# 1- k
# 2- u
# 3- l
# 4- d
# 5- a
# 6- y
# 7- k
# 8- e
# 9- n    