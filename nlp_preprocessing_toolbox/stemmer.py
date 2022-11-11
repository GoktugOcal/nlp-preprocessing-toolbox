# from nlp_preprocessing_toolbox.helper import *
from nlp_preprocessing_toolbox.data.roots import *
from nlp_preprocessing_toolbox.data.suffixes import *
import re

'''
import io
f = io.open("nlp_preprocessing_toolbox/data/suffixes.txt", mode="r", encoding="utf-8")
txt = f.read()

import json

suffix_dict = {}
for item in txt.split(";"):
    items = item.split('\t')
    suff = items[0].replace("*","").replace("-","").strip()
    if suff:
        suffix_dict[suff] = (items[-1].split(",")[0], items[-1])

suffix_list = []
for item in suffix_dict.items():
    suffix_list.append(item)

suffix_list = sorted(suffix_list, key = lambda x: x[1][0])
SUFFIXES = []
for item in suffix_dict.items():
    SUFFIXES.append(Suffix(item[1], item[0].replace("-",""), None, False))
'''

class State:
    def __init__(self, word, suffix):
        self.word = word
        self.suffix = suffix
        self.parent = None
        
    def setChild(self, state):
        self.parent = state
    
    def findStem(self, suffix_list, stem_list, i):

        if self.word in stem_list:
            return self.word

        stems = []
        for suff_type in suffix_list:
            for suff in suff_type:
                match = suff.Match(self.word)
                if match != None:
                    new_word = suff.RemoveSuffix(self.word)
                    new_state = State(new_word, match.group())
                    stem = new_state.findStem(suffix_list, stem_list, i+1)
                    stems.append(stem)
        
        stems = [stem for stem in stems if stem != None]
        stems = sorted(stems, key = lambda x: len(x))
        if stems: return stems[0]
        else: return None

#########################

class Stemmer:
    def __init__(self):
        self.words = None
        self.suffixes = self.load_suffixes()
        self.roots = self.load_roots()
    
    def load_suffixes(self):
        return [DERIVATIONAL_SUFFIXES, NOMINAL_VERB_SUFFIXES, NOUN_SUFFIXES]

    def load_roots(self):
        return roots
        
    def setText(self, text):
        if type(text) == list: 
            stems = []
            for word in text:
                word = word.lower()
                initial_state = State(word, None)
                stem = initial_state.findStem(self.suffixes, self.roots, 1)
                if stem == None: stems.append(word)
                else: stems.append(stem)
            self.stems = stems

        elif type(text) == str:
            text = text.lower()
            initial_state = State(text, None)
            stem = initial_state.findStem(self.suffixes, self.roots, 1)
            if stem == None: self.stems = text
            else: self.stems = stem
        
        else:
            raise TypeError("text type is not supported. text should be list or string.")