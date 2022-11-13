import requests

def stopword_elimination(text_list):

    res = requests.get('https://raw.githubusercontent.com/ahmetax/trstop/master/dosyalar/turkce-stop-words')
    stopword_list = res.text.split("\n")
    stopword_list.append(" ")

    eliminated_list = []
    
    for word in text_list:
        if word not in stopword_list: eliminated_list.append(word)
        
    return eliminated_list