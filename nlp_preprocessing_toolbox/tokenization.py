from nlp_preprocessing_toolbox.data.regex_patterns import *
import re

class Tokenization:
    def __init__(self, text):
        self.text = text

    def __regex_finder(self, regex_list: list):
        for regex in regex_list:
            for matches in re.finditer(regex, self.text, flags=re.IGNORECASE | re.DOTALL):
                yield matches
        
    def run(self):
        for regex_list, r_types in all_regex:
            print(regex_list, "||", r_types)
            for mathes in self.__regex_finder(regex_list):
                print(mathes.span())