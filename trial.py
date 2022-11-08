from nlp_preprocessing_toolbox.tokenization import Tokenization
from nlp_preprocessing_toolbox.sentence_splitter import SentenceSplitter



text = '''Saçma ve Gereksiz Bir Yazı.
Bakkaldan 5 TL'lik 2 çikola-
ta al. 12.02.2018 tarihinde saat tam 15:45'te yap-
malıyız bu işi. Tamam mı? Benimle esatmahmutbayol@gmail.com 
adresinden iletişime geçebilirsin. Yarışta 1. oldu. Doç. Dr. 
Esat Bayol'un(Böyle bir ünvanım yok!) yanından geliyorum.
12 p.m. mi yoksa 12 a.m. mi? 100 milyon insan gelmiş! www.deneme.com.tr 
adresinden sitemizi inceleyebilirsin. 24 Eylül 2018 Pazartesi günü ge-
lecekmiş. 19 Mayıs'ı coşkuyla kutladık.
Sonra dedi ki "Ben seni sevmiyorum."'''

text = '''Saçma ve Gereksiz Bir Yazı.
Bakkaldan 5 TL'lik 2 çikola-

ta al.'''


#with open("nlp_preprocessing_toolbox/data/UD_Turkish-BOUN/tr_boun-ud-test.txt", encoding="utf-8") as f:
#    text = f.read()
'''
tokenizer = Tokenization(text)
tokenizer.run()
print(tokenizer.spans)
print()
print(tokenizer.tokens)

print('Done.')
'''

tokenizer = Tokenization(text)
splitter = SentenceSplitter(text)
splitter.run(tokenizer)
print(splitter.sentences)
print(splitter.sentences_types)


print('Done.')