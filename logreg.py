from sklearn import linear_model, metrics
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import string


df = pd.read_csv('example.csv')
df = df.astype(int)

train_test_split = int(len(df)*0.8)
dfTrain, dfTest = df[0:train_test_split], df[train_test_split:]

X_train = dfTrain.values[:,0:-1]
y_train = dfTrain.values[:,-1]

X_test = dfTest.values[:,0:-1]
y_test = dfTest.values[:,-1]


logr = linear_model.LogisticRegression()
logr.fit(X_train,y_train)


confusion_matrix = metrics.plot_confusion_matrix(logr, X_test, y_test, cmap = "GnBu")
plt.show()


text = '''Çünkü ben de o yaşadığı çevreyi kirleterek bozulmasına neden olan, tüm uyarılara
kulağını tıkayan soya aitim. Kimileri buna kader diyordu, kimileri unut. Bu da
zaman ister, emek ister. İki veli dokunulsa ağlayacaktı. Bu meslek böyledir.
Filmde kamburunu çıkarmış eski Yugoslav lideri, iki kişinin arasında elleri
önden bağlı, cezaevi avlusunda yürüyor. Sabahları hiçbir şey yemeden içmeden,
paldür küldür çıkıyorum evden. Bu albüm hit şarkı çıkarmaz, dedim.'''

text = " " + text.replace("\n", " ") + " "
lines = []
for idx, char in enumerate(text):

    isItPunc, isItWhitespace, isNextWhitespace, isPrevNumber, isNextNumber, isNextPunc = False, False, False, False, False, False
    
    if char != " " and idx != 0 and idx != len(text)-1:
        if char in string.punctuation                   : isItPunc = True
        if text[idx+1] == " "                           : isNextWhitespace = True
        if text[idx-1].isnumeric()                      : isPrevNumber = True
        if text[idx+1].isnumeric()                      : isNextNumber = True
        if text[idx+1] in string.punctuation            : isNextPunc = True

        row = {
                "char" : char,
                "#is it punctuation" : isItPunc,
                "#is it whitespace" : isItWhitespace,
                "#is next whitespace" : isNextWhitespace,
                "#is previos char number" : isPrevNumber,
                "#is next char number" : isNextNumber,
                "#is next char punc" : isNextPunc,
        }
        lines.append(row)

df = pd.DataFrame.from_records(lines)
print(df)