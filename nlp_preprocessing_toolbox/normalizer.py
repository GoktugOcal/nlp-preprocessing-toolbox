from nlp_preprocessing_toolbox.tokenizer import * 
from nlp_preprocessing_toolbox.data.regex_patterns import *
from nlp_preprocessing_toolbox.helper import *
from nlp_preprocessing_toolbox.data.chars import *
from itertools import product, groupby
import bz2
import pickle
import re

class Normalizer():
    def __init__(self):
        self.text = ""
        self.word_list = []
        self.load_freq_dict()

    def load_freq_dict(self):
        data = bz2.BZ2File("nlp_preprocessing_toolbox/data/freq_dict.pbz2", "rb")
        data = pickle.load(data)
        self.freq_dict = data

    def setText(self, text, tokenizer=None):
        
        self.text = text

        if tokenizer == None:
            tokenizer = Tokenizer()

        tokenizer.setText(text)
        tokenizer.run()
        self.word_list = tokenizer.tokens

    def createVariations(self, word):

        a1 = ['', 'a', 'e', 'ı', 'i', 'o', 'ö', 'u', 'ü']

        if word[0] in allVowels:
            result = [word[0]]
        else:
            result = [a1, word[0]]

        for i in range(1, len(word)):
            fl = word[i - 1]
            fs = word[i]

            if (fl not in allVowels) and (fs not in allVowels):
                result.append(a1)
                result.append(fs)
            else:
                result.append(fs)
        
        return [''.join(x) for x in product(*result)]
        
    def __known(self, words):
        known_list = []
        for w in words:
            if w in self.freq_dict:
                known_list.append(w)
        return known_list

    def run(self):

        for word in self.word_list:
            variations = self.createVariations(word.lower())
            print(variations)
            #print(word, " - ", self.__known([word.lower()]))


