from nlp_preprocessing_toolbox import *
from nlp_preprocessing_toolbox.data.regex_patterns import *
from nlp_preprocessing_toolbox.helper import *
import numpy as np
import re

class SentenceSplitter:
    def __init__(self, text):
        self.text = text
        self.sentences = []
        self.sentences_tokens = []
        self.sentences_types = []
        self.sentences_spans = []


    def __fixation(self):
        
        self.text = unitoascii(self.text).replace("''", '"')
        self.text = '\n'.join([line for line in self.text.split('\n') if line.strip() != '']) #remove empty lines
        self.text = re.sub(' +', ' ', self.text) #reduce multiple whitespaces to one

        splitted_text = self.text.split("\n")
        for idx in range(len(splitted_text)):
            if splitted_text[idx].endswith("-"):
                next_item = splitted_text[idx+1].split(" ")
                splitted_text[idx] = splitted_text[idx].replace("-",next_item[0])
                splitted_text[idx + 1] = splitted_text[idx + 1].replace(next_item[0],"").lstrip()
        
        self.text = "\n".join(splitted_text)

    def __regex_finder(self, regex_list: list):
        for regex in regex_list:
            for matches in re.finditer(regex, self.text, flags=re.IGNORECASE | re.DOTALL):
                yield matches
        
    def run(self, tokenizer=None):

        if tokenizer == None: tokenizer = Tokenizer()

        tokenizer.setText(self.text)
        tokenizer.run()
        temp_sentence = []
        temp_sentences_types = []
        temp_sentences_spans = []
        for idx in range(len(tokenizer.types)):

            if not tokenizer.types[idx] in ["enter"]:
                temp_sentence.append(tokenizer.tokens[idx])
                temp_sentences_types.append(tokenizer.types[idx])
                temp_sentences_spans.append(tokenizer.spans[idx]) 

                if tokenizer.types[idx] == "eos":
                    self.sentences_tokens.append(temp_sentence)
                    self.sentences_types.append(temp_sentences_types)
                    self.sentences_spans.append(temp_sentences_spans)

                    temp_sentence = []
                    temp_sentences_types = []
                    temp_sentences_spans = []
            '''
            elif tokenizer.types[idx] == "enter":
                temp_sentence.append(" ")
                temp_sentences_types.append("space")
                temp_sentences_spans.append(tokenizer.spans[idx]) 
            '''
        for sentence_token in self.sentences_tokens:
            self.sentences.append("".join(sentence_token))
        '''
        else:
            self.__fixation()
            for regex_list, token_type in [(end_of_seq,"eos")]:
                for matches in self.__regex_finder(regex_list):
                    self.spans.append(matches.span())
                    self.types.append(token_type)

            #select spans (there could be multiple tokens in same position in regexing)

            span_set = set()
            spans,types = [],[]
            for s in range(len(self.spans)):
                s_type = self.types[s]
                x, y = self.spans[s]
                if x == y: continue
                elif (y-x == 1) and (x not in span_set):
                    spans.append((x, y))
                    types.append(s_type)
                    span_set.add(x)
                else:
                    in_span_set = [i for i in range(x,y) if i in span_set]                    
                    if not in_span_set:
                        spans.append((x, y))
                        types.append(s_type)
                        [span_set.add(x) for x in range(x, y)]
            
            #sort tokens and types by span indexes
            spans_type = list(zip(spans, types))
            spans_type.sort(key=lambda l: l[0][0])
            self.spans = [x for x, y in spans_type]
            self.types = [y for x, y in spans_type]

            #set tokens
            self.tokens = [self.text[self.spans[i][0]:self.spans[i][1]] for i in range(len(self.spans))]
        '''
        print("Sentence splitting is done...")