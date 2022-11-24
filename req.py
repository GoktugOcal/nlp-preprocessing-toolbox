text = '''
cak|cek
cağız|ceğiz
cık|cik|cuk|cük
ar|er|şar|şer
cıl|cıl|çıl|çil
daş|taş
gil|giller
sısi|su|sü
(ı)msı|(i)msi|(u)msu|(u)msü
mtrak
tı|ti|tu|tü
sal|sel
(ı)ncı|(i)nci
aç|eç
ç
ak|ek
k
an|en
z
l
kan
n|ın|in|unün
t
sıl|sil|sul|sül
ş
aş|eş
şın|şin
ar|er|şar|şer
ay|ey
dırık|dirik|duruk|dürük
ca|ce|ça|çe
'''
i = 3
for line in text.split("\n"):
    tag = "-"+line.split("|")[0]
    print('GD' + str(i) + '= Suffix("' + tag + '", "' + line + '", None, True)')
    i += 1