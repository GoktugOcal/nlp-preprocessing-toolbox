from nlp_preprocessing_toolbox.tokenizer import * 
from nlp_preprocessing_toolbox.data.regex_patterns import *
from nlp_preprocessing_toolbox.helper import *
from nlp_preprocessing_toolbox.data.chars import *
from itertools import product, groupby
import bz2
import pickle
import re
import numpy as np

class Normalizer():
    def __init__(self):
        self.text = ""
        self.word_list = []
        self.new_words = []
        self.load_freq_dict()

    def load_freq_dict(self):
        data = bz2.BZ2File("nlp_preprocessing_toolbox/data/freq_dict.pbz2", "rb")
        data = pickle.load(data)
        self.freq_dict = data

    def setText(self, text, tokenizer=None):

        if tokenizer == None:
            tokenizer = Tokenizer()

        if type(text) == list:
            self.word_list = text

        elif type(text) == str:
            self.word_list = tokenizer.setText(text).run().tokens

        self.run()

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
        
    def find_known(self, words):
        known_list = []
        freq_list = []
        for w in words:
            if w in self.freq_dict:
                known_list.append(w)
                freq_list.append(self.freq_dict[w])
        return dict(zip(known_list, freq_list))

    def run(self):

        for word in self.word_list:
            variations = self.createVariations(word.lower())
            known = self.find_known(variations)
            similars = []

            for x in known.items():
                edit_dist = levenshtein_distance(word, x[0])
                similars.append((x[0], edit_dist, x[1]))

            if similars:
                sorted_list = sorted(similars, key= lambda x: x[1])
                new_word = sorted(list(filter(lambda x: x[1]== sorted_list[0][1], sorted_list)), key= lambda x: x[1])[0]
                self.new_words.append(new_word[0])

            else:
                self.new_words.append(word)