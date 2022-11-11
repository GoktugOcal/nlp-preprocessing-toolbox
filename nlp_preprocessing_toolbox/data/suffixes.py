import re

class Suffix(object):
    def __init__(self, name, pattern, optionalLetter, checkHarmony):
        self.name = name
        self.pattern = re.compile("(" + pattern + ")$", re.UNICODE)

    def Match(self, word):
        return self.pattern.search(word)

    def RemoveSuffix(self, word):
        return self.pattern.sub("", word)

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
NOUN_SUFFIXES = (S16,S7,S3,S5,S1,S14,S15,S17,S10,S19,S4,S9,S12,S13,S18,S2,S6,S8,S11)