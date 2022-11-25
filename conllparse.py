import conllu
import string
import pandas as pd
from tqdm import tqdm

data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-BOUN/tr_boun-ud-train.conllu", "r", encoding="utf-8")
# data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-Penn/tr_penn-ud-train.conllu", "r", encoding="utf-8")

text = data_file.read()

df = pd.DataFrame()

lines = []

for item in tqdm(conllu.parse(text)):
    text = " "
    labels = ""
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

        isItPunc, isItPeriod, isItWhitespace, isNextWhitespace, isPrevNumber, isNextNumber, isNextPunc, isItNum, isNextPeriod = \
            False, False, False, False, False, False, False, False, False
        token = item[i]["form"]
        try:
            if item[i]["misc"]["SpaceAfter"] == "No": pass
            else: token = token + " "
        except:
            token = token + " "

        for ch_idx in range(len(item[i]["form"])):

            char = token[ch_idx]

            ########### if item is the last token in the sentence
            if i == len(item)-1: 
                if ch_idx == len(token)-1 and ch_idx == 0: # if token has single char
                    if char in string.punctuation                       : isItPunc = True
                    if char == "."                                      : isItPeriod = True
                    if char.isnumeric()                                 : isItNum = True
                    # if char == " "                                      : isItWhitespace = True
                    isNextWhitespace = True
                    isNextPeriod = False
                    if text[-1].isnumeric()                             : isPrevNumber = True

                elif ch_idx == 0: # if char is first char
                    if char in string.punctuation                       : isItPunc = True
                    if char == "."                                      : isItPeriod = True
                    if char.isnumeric()                                 : isItNum = True
                    # if char == " "                                      : isItWhitespace = True
                    isNextWhitespace = True
                    if token[ch_idx+1] == "."                           : isNextPeriod = True
                    if text[-1].isnumeric()                             : isPrevNumber = True
                
                elif ch_idx == len(token)-1: #if char is last char
                    if char in string.punctuation                       : isItPunc = True
                    if char == "."                                      : isItPeriod = True
                    if char.isnumeric()                                 : isItNum = True
                    # if char == " "                                      : isItWhitespace = True
                    isNextWhitespace = True
                    isNextPeriod = True
                    if token[ch_idx-1].isnumeric()                      : isPrevNumber = True
                
                else:
                    if char in string.punctuation                       : isItPunc = True
                    if char == "."                                      : isItPeriod = True
                    if char.isnumeric()                                 : isItNum = True
                    # if char == " "                                      : isItWhitespace = True
                    if token[ch_idx+1] == " "                           : isNextWhitespace = True
                    if token[ch_idx+1] == "."                           : isNextPeriod = True
                    if token[ch_idx-1].isnumeric()                      : isPrevNumber = True
                    if token[ch_idx+1].isnumeric()                      : isNextNumber = True
                    if token[ch_idx+1] in string.punctuation            : isNextPunc = True

            ########### if item is not the last
            else:
                if ch_idx == len(token)-1 and ch_idx == 0: # if token has single char
                    if char in string.punctuation                       : isItPunc = True
                    if char == "."                                      : isItPeriod = True
                    if char.isnumeric()                                 : isItNum = True
                    # if char == " "                                      : isItWhitespace = True
                    if item[i+1]["form"][0] == " "                      : isNextWhitespace = True
                    if text[-1].isnumeric()                             : isPrevNumber = True
                    if item[i+1]["form"][0].isnumeric()                 : isNextNumber = True
                    if item[i+1]["form"][0] in string.punctuation       : isNextPunc = True

                elif ch_idx == 0:
                    if char in string.punctuation                       : isItPunc = True
                    if char == "."                                      : isItPeriod = True
                    if char.isnumeric()                                 : isItNum = True
                    # if char == " "                                      : isItWhitespace = True
                    if token[ch_idx+1] == " "                           : isNextWhitespace = True
                    if token[ch_idx+1] == "."                           : isNextPeriod = True
                    if text[-1].isnumeric()                             : isPrevNumber = True
                    if token[ch_idx+1].isnumeric()                      : isNextNumber = True
                    if token[ch_idx+1] in string.punctuation            : isNextPunc = True
                
                elif ch_idx == len(token)-1:
                    if char in string.punctuation                       : isItPunc = True
                    if char == "."                                      : isItPeriod = True
                    if char.isnumeric()                                 : isItNum = True
                    # if char == " "                                      : isItWhitespace = True
                    if item[i+1]["form"][0] == " "                      : isNextWhitespace = True
                    if item[i+1]["form"][0] == "."                      : isNextPeriod = True
                    if item[i]["form"][ch_idx-1].isnumeric()            : isPrevNumber = True
                    if item[i+1]["form"][0].isnumeric()                 : isNextNumber = True
                    if item[i+1]["form"][0] in string.punctuation       : isNextPunc = True
                
                else:
                    if char in string.punctuation                       : isItPunc = True
                    if char == "."                                      : isItPeriod = True
                    if char.isnumeric()                                 : isItNum = True
                    # if char == " "                                      : isItWhitespace = True
                    if token[ch_idx+1] == " "                           : isNextWhitespace = True
                    if token[ch_idx+1] == "."                           : isNextPeriod = True
                    if token[ch_idx-1].isnumeric()                      : isPrevNumber = True
                    if token[ch_idx+1].isnumeric()                      : isNextNumber = True
                    if token[ch_idx+1] in string.punctuation            : isNextPunc = True


            if ch_idx == len(item[i]["form"])-1: label = 1
            else: label = 0

            row = {
                "char" : char,
                "#is it number" : isItNum,
                "#is it punctuation" : isItPunc,
                "#is it period" : isItPeriod,
                "#is next whitespace" : isNextWhitespace,
                "#is previos char number" : isPrevNumber,
                "#is next char number" : isNextNumber,
                # "#is next char punc" : isNextPunc,
                "#is next char period" : isNextPeriod,
                "label": label
            }

            # ########### if last token
            # if i == len(item)-1: 
            #     if ch_idx == len(token)-1 and ch_idx == 1: # if token has single char
            #         prev_char = item[i-1]["form"][-1]
            #         next_char = item[i+1]["form"][0]

            #     elif ch_idx == 0: # if char is first char
            #         prev_char = item[i-1]["form"][-1]
            #         next_char = token[ch_idx+1]
                
            #     elif ch_idx == len(token)-1: #if char is last char
            #         prev_char = token[ch_idx-1]
            #         next_char = " "
            #     else:
            #         prev_char = token[ch_idx-1]
            #         next_char = token[ch_idx+1]

            # ########### if first token
            # if i == 0: 
            #     if ch_idx == len(token)-1 and ch_idx == 1: # if token has single char
            #         prev_char = " "
            #         next_char = item[i+1]["form"][0]

            #     elif ch_idx == 0: # if char is first char
            #         prev_char = " "
            #         next_char = token[ch_idx+1]
                
            #     elif ch_idx == len(token)-1: #if char is last char
            #         prev_char = token[ch_idx-1]
            #         next_char = " "
            #     else:
            #         prev_char = token[ch_idx-1]
            #         next_char = token[ch_idx+1]

            # ########### if item is not the last
            # else:
            #     if ch_idx == len(token)-1 and ch_idx == 0: # if token has single char
            #         prev_char = " "
            #         next_char = item[i+1]["form"][0]
            #     elif ch_idx == 0: # if char is first char
            #         prev_char = item[i-1]["form"][-1]
            #         next_char = token[ch_idx+1]
            #     elif ch_idx == len(token)-1: #if char is last char
            #         prev_char = token[ch_idx-1]
            #         next_char = item[i+1]["form"][0]
            #     else:
            #         prev_char = token[ch_idx-1]
            #         next_char = token[ch_idx+1]


                

            # row = {
            #     "char" : char,
            #     "next_char" : ,
            #     "prev_char" : ,
                
            # }
            lines.append(row)
        #########################

        try:
            if item[i]["misc"]["SpaceAfter"] == "No":
                text = text + item[i]["form"]
            else:
                text = text + item[i]["form"] + item[i]["misc"]["SpacesAfter"]
        except Exception as e:
            # print(e)
            text = text + item[i]["form"] + " "

        # input()


df = pd.DataFrame.from_records(lines)
df.to_csv("example.csv",index=False)
