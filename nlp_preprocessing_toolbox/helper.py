from difflib import ndiff
import re
import conllu
import string
import pandas as pd
from tqdm import tqdm

def __fixation(text):
        
        text = unitoascii(text).replace("''", '"')
        text = '\n'.join([line for line in text.split('\n') if line.strip() != '']) #remove empty lines
        text = re.sub(' +', ' ', text) #reduce multiple whitespaces to one

        splitted_text = text.split("\n")
        for idx in range(len(splitted_text)):
            if splitted_text[idx].endswith("-"):
                next_item = splitted_text[idx+1].split(" ")
                splitted_text[idx] = splitted_text[idx].replace("-",next_item[0])
                splitted_text[idx + 1] = splitted_text[idx + 1][len(next_item[0]):]
                # print(next_item[0])
                #.replace(next_item[0],"")
        
        text = "\n".join(splitted_text)
        return text

def levenshtein_distance(str1, str2, ):
    counter = {"+": 0, "-": 0}
    distance = 0
    for edit_code, *_ in ndiff(str1, str2):
        if edit_code == " ":
            distance += max(counter.values())
            counter = {"+": 0, "-": 0}
        else: 
            counter[edit_code] += 1
    distance += max(counter.values())
    return distance

def to_lower(word: str):
    tolower_text = (word.replace('İ', 'i'))
    tolower_text = (tolower_text.replace('I', 'ı'))
    return tolower_text.lower()


def _decode(string: str) -> str:
    """
    Bu fonksiyon unidecode kütüphanesinden alınmış ve türkçe için özelleştirilmiştir.
    Türkçe için genişletilmiş Ascii çevirici.
    :param string: unicode string
    :return: Tr Ascii string
    """
    cache = {}
    decval = []

    for char in string:
        codepoint = ord(char)

        if codepoint in {199, 214, 220, 231, 246, 252, 286, 287, 304, 305, 350, 351, 8364, 8378, 8240}:
            decval.append(str(char))
            continue

        if codepoint < 0x80:
            decval.append(str(char))
            continue

        if codepoint > 0xeffff:
            continue

        section = codepoint >> 8
        position = codepoint % 256

        if section in cache:
            table = cache[section]
        else:
            try:
                mod = __import__('unidecoder.x%03x' % section, fromlist=['data'])
            except ImportError:
                cache[section] = None
                continue
            cache[section] = table = mod.data

        if table and len(table) > position:
            decval.append(table[position])

    return ''.join(decval)

def unitoascii(string: str) -> str:
    """
    Türkçe için genişletilmiş Ascii çevirici.
    :param string: unicode string
    :return: Tr Ascii string
    """
    try:
        string.encode('ASCII')
    except UnicodeEncodeError:
        return _decode(string)

    return string



def tokenizer_load_and_parse_corpus(save = False):

    print("\tParsing the corpus.")
    data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-BOUN/tr_boun-ud-train.conllu", "r", encoding="utf-8")
    # data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-Penn/tr_penn-ud-train.conllu", "r", encoding="utf-8")

    text = data_file.read()

    df = pd.DataFrame()

    lines = []

    new_text = " "
    labels = []
    for item in tqdm(conllu.parse(text)):
        last_id = 0
        for i in range(len(item)):
            
            if type(item[i]["id"]) == tuple:
                if item[i]["id"][0] > last_id: valid = True
                else: continue
            else:
                if item[i]["id"] > last_id: valid = True
                else: continue

            if type(item[i]["id"]) == tuple: last_id = item[i]["id"][-1]
            else: last_id = item[i]["id"]

            ##########################
            token = item[i]["form"]
            iter_len = len(token)
            

            for idx in range(iter_len):

                if idx == iter_len-1: label = 1
                else: label = 0
                new_text += token[idx]
                
                labels.append(label)
                
                row = {
                    "char" : token[idx],
                    "label" : label
                }
                lines.append(row)
                
            try:
                if item[i]["misc"]["SpaceAfter"] == "No": pass
                else: 
                    new_text = new_text + " "
                    row = {
                        "char" : " ",
                        "label" : 0
                    }
                    lines.append(row)
            except:
                new_text = new_text + " "
                row = {
                    "char" : " ",
                    "label" : 0
                }
                lines.append(row)

    df_raw = pd.DataFrame.from_records(lines)
    if save: df_raw.to_csv("nlp_preprocessing_toolbox/data/tokenizer_parsed.csv", index=False)

    return df_raw

def logistic_regression_preprocesing(df_raw):

    df_raw["t-1"] = df_raw.char.shift(1)
    df_raw["t-2"] = df_raw.char.shift(2)
    df_raw["t+1"] = df_raw.char.shift(-1)
    df_raw["t+2"] = df_raw.char.shift(-2)

    for col in ["char", "t-1", "t-2", "t+1", "t+2"]:
        df_raw[col + "_punc"] = [True if (str(val) in string.punctuation) else False for val in df_raw[col].values]
        df_raw[col + "_num"] = [True if (str(val).isnumeric()) else False for val in df_raw[col].values]    
        df_raw[col + "_space"] = [True if (str(val) == " ") else False for val in df_raw[col].values]    
        df_raw[col + "_period"] = [True if (str(val) == "." ) else False for val in df_raw[col].values]
        
    df_raw = df_raw.dropna()

    req_cols = ["char"]
    for col in ["char", "t-1", "t-2", "t+1", "t+2"]:
        for suff in ["_punc", "_num", "_space", "_period"]:
            req_cols.append(col+suff)

    try:
        req_cols_2 = req_cols + ["label"]
        df = df_raw[req_cols_2]
    except:
        df = df_raw[req_cols]

    df_now = df[df.columns[1:]]
    df_now = df_now.astype(int)
    
    return df, df_now



############# Sentence Splitting Tools


def sentence_splitter_load_and_parse_corpus(save = False):

    print("\tParsing the corpus.")
    data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-BOUN/tr_boun-ud-train.conllu", "r", encoding="utf-8")
    # data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-Penn/tr_penn-ud-train.conllu", "r", encoding="utf-8")

    text = data_file.read()

    df = pd.DataFrame()

    lines = []

    new_text = " "
    labels = []

    for item in tqdm(conllu.parse(text)):
        last_id = 0
        for i in range(len(item)):
            
            if type(item[i]["id"]) == tuple:
                if item[i]["id"][0] > last_id: valid = True
                else: continue
            else:
                if item[i]["id"] > last_id: valid = True
                else: continue

            if type(item[i]["id"]) == tuple: last_id = item[i]["id"][-1]
            else: last_id = item[i]["id"]

            ##########################
            token = item[i]["form"]
            iter_len = len(token)
            

            for idx in range(iter_len):

                if idx == iter_len-1 and i == len(item)-1: label = 1
                else: label = 0
                new_text += token[idx]
                
                labels.append(label)
                
                row = {
                    "char" : token[idx],
                    "label" : label
                }
                lines.append(row)
                
            try:
                if item[i]["misc"]["SpaceAfter"] == "No": pass
                else: 
                    new_text = new_text + " "
                    row = {
                        "char" : " ",
                        "label" : 0
                    }
                    lines.append(row)
            except:
                new_text = new_text + " "
                row = {
                    "char" : " ",
                    "label" : 0
                }
                lines.append(row)

    df_raw = pd.DataFrame.from_records(lines)
    if save: df_raw.to_csv("nlp_preprocessing_toolbox/data/sentence_splitter_parsed.csv", index=False)

    return df_raw

def naive_bayes_preprocessing(df_raw):
    time_lags = [-1,+1]

    for col in time_lags:
        if col >= 0: df_raw["t+"+str(col)] = df_raw.char.shift(col)
        else: df_raw["t"+str(col)] = df_raw.char.shift(col)

    df_raw = df_raw.dropna()
    
    time_lags = [-1,1] 
    for col in time_lags:
        if col >= 0: df_raw["t+"+str(col)] = df_raw["t+"+str(col)].astype(str)
        else: df_raw["t"+str(col)] = df_raw["t"+str(col)].astype(str)

    df_raw["char"] = df_raw["char"].astype(str)
    df_raw["text"] = [row["t-1"] + row["char"] + row["t+1"] for i, row in df_raw.iterrows()]
    
    return df_raw