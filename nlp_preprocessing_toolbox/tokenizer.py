from nlp_preprocessing_toolbox.data.regex_patterns import *
from nlp_preprocessing_toolbox.helper import *
import numpy as np
import re

from sklearn import linear_model, metrics
import pandas as pd
import string

with open("nlp_preprocessing_toolbox/data/abrv.txt", "r", encoding="utf-8") as abrv_file:
    text = abrv_file.read()
    abrv_list = [line.split("\t")[0] for line in text.split("\n")]
    
class Tokenizer:
    def __init__(self):
        self.text = ""
        self.tokens = []
        self.spans = []
        self.types = []

    def setText(self, text):
        self.text = text


    def __fixation(self):
        
        self.text = unitoascii(self.text).replace("''", '"')
        self.text = '\n'.join([line for line in self.text.split('\n') if line.strip() != '']) #remove empty lines
        self.text = re.sub(' +', ' ', self.text) #reduce multiple whitespaces to one

        splitted_text = self.text.split("\n")
        for idx in range(len(splitted_text)):
            if splitted_text[idx].endswith("-"):
                next_item = splitted_text[idx+1].split(" ")
                splitted_text[idx] = splitted_text[idx].replace("-",next_item[0])
                splitted_text[idx + 1] = splitted_text[idx + 1][len(next_item[0]):]
                # print(next_item[0])
                #.replace(next_item[0],"")
        
        self.text = "\n".join(splitted_text)

    def __regex_finder(self, regex_list: list):
        for regex in regex_list:
            for matches in re.finditer(regex, self.text, flags=re.IGNORECASE | re.DOTALL):
                yield matches
        
    def run(self):
        self.__fixation()
        for regex_list, token_type in all_regex:
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

        spans_type_last = []
        for i in range(len(spans_type)):
            if spans_type[i][1] == "eos" and spans_type[i-1][1] == "word":
                if self.text[spans_type[i-1][0][0]:spans_type[i][0][1]].lower().replace(" " ,"") in abrv_list:
                    spans_type_last.pop()
                    spans_type_last.append(((spans_type[i-1][0][0],spans_type[i][0][1]),"word"))
                else: spans_type_last.append(spans_type[i])
            else: spans_type_last.append(spans_type[i])

        self.spans = [x for x, y in spans_type_last]
        self.types = [y for x, y in spans_type_last]

        #set tokens
        self.tokens = [self.text[self.spans[i][0]:self.spans[i][1]] for i in range(len(self.spans))]

        print("Tokenization is done...")


class TokenizerML():

    def __init__(self):
        self.text = ""
        self.tokens = []

    def setText(self, text):
        self.text = text

    def __fixation(self):
        
        self.text = unitoascii(self.text).replace("''", '"')
        self.text = '\n'.join([line for line in self.text.split('\n') if line.strip() != '']) #remove empty lines
        self.text = re.sub(' +', ' ', self.text) #reduce multiple whitespaces to one

        splitted_text = self.text.split("\n")
        for idx in range(len(splitted_text)):
            if splitted_text[idx].endswith("-"):
                next_item = splitted_text[idx+1].split(" ")
                splitted_text[idx] = splitted_text[idx].replace("-",next_item[0])
                splitted_text[idx + 1] = splitted_text[idx + 1][len(next_item[0]):]
                # print(next_item[0])
                #.replace(next_item[0],"")
        
        self.text = "\n".join(splitted_text)

    def run(self):
        self.__fixation()

        df_raw = tokenizer_load_and_parse_corpus()
        df_raw, df = logistic_regression_preprocesing(df_raw)

        train_test_split = int(len(df)*0.8)
        dfTrain, dfTest = df[0:train_test_split], df[train_test_split:]

        X_train = dfTrain.values[:,0:-1]
        y_train = dfTrain.values[:,-1]

        X_test = dfTest.values[:,0:-1]
        y_test = dfTest.values[:,-1]

        print("\tTraining the model...")
        logr = linear_model.LogisticRegression()
        logr.fit(X_train,y_train)

        print("\tTokenizing...")
        text = "  " + self.text.replace("\n", " ") + "  "
        lines = []
        for idx, char in enumerate(text):
            row = {
                "char" : char
            }
            lines.append(row)
            
        df_text = pd.DataFrame.from_records(lines)
        df_text, df_real_test = logistic_regression_preprocesing(df_text)

        df_real_test = df_real_test.values
        
        pred = logr.predict(df_real_test)
        df_text["label"] = pred

        tokens = []
        last_idx = 0
        temp = ""
        for idx, row in df_text.iterrows():
            if row.label == 0: temp += row.char
            elif row.label == 1:
                temp += row.char
                tokens.append(temp)
                temp = ""
                last_idx = idx

        self.tokens = tokens