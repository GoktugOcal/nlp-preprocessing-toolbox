from nlp_preprocessing_toolbox.tokenizer import *
from nlp_preprocessing_toolbox.data.regex_patterns import *
from nlp_preprocessing_toolbox.helper import *
import numpy as np
import re

import math
import string


class SentenceSplitter:
    def __init__(self):
        self.text = ""
        self.sentences = []
        self.sentences_tokens = []
        self.sentences_types = []
        self.sentences_spans = []

    def setText(self,text):
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

        for sentence_token in self.sentences_tokens:
            self.sentences.append("".join(sentence_token))
 
        print("Sentence splitting is done...")

class SentenceSplitterML:
    def __init__(self):
        self.text = ""
        self.sentences = []
    
    def setText(self,text):
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

        df_raw = sentence_splitter_load_and_parse_corpus()
        df_raw = naive_bayes_preprocessing(df_raw)

        time_cols = []
        for col in [-1,1]:
            if col >= 0: time_cols.append("t+"+str(col))
            else: time_cols.append("t"+str(col))

        punc_df = df_raw[df_raw["char"].isin(list(string.punctuation))].reset_index(drop=True)

        prob_df = pd.DataFrame(columns = sorted(list(set(punc_df[["char"] + time_cols].values.reshape(-1,1).T[0])), key = lambda x: x), index = [0,1])
        p_cls = {
            0:len(punc_df[punc_df.label == 0]) / len(punc_df),
            1:len(punc_df[punc_df.label == 1]) / len(punc_df)
        }

        # Training
        print("\tTraining")
        for idx in prob_df.index:
            df_class = punc_df[punc_df.label == idx]
            chars = df_class[["char"] + time_cols].values.reshape(-1,1).T[0]
            no_uniq_chars = len(set(chars))
            total_c = len(chars)
            
            for col in prob_df.columns:
                char_c = len(chars[chars == col])
                prob_df.iloc[idx][col] = math.log((char_c + 1) / (total_c + no_uniq_chars)) + math.log(p_cls[idx])

        #Preparing Test Data
        text = " " + self.text.replace("\n", " ") + " "

        lines = []
        for idx, char in enumerate(text):
            row = {
                "char" : char
            }
            lines.append(row)

        df_text = pd.DataFrame.from_records(lines)
        df_text = naive_bayes_preprocessing(df_text)
        preds = []
        prob_dict = prob_df.to_dict()

        #Predicting
        print("\tPredicting")
        for idx, row in tqdm(df_text.iterrows(), total=len(df_text)):
            if row["char"] in list(string.punctuation):
                try:
                    char_prob_dict = {}
                    for cls in [0,1]:
                        values = list(map(lambda x: prob_dict[x][cls], list(row.text)))
                        char_prob_dict[cls] = np.prod(values)
                    preds.append(max(char_prob_dict, key=char_prob_dict.get))
                except:
                    preds.append(0)
            else:
                preds.append(0)

        df_text["label"] = preds

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

        self.sentences = tokens

        print("Sentence splitting is done...")

