data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-BOUN/tr_boun-ud-train.conllu", "r", encoding="utf-8")
text = data_file.read()

idx = 0
dot_sent = []
sentences = []

eos = []
punc = []
for line in text.split("\n"):
    if "#" in line and "text = " in line:
        sentence = line.split(" = ")[1]
        # if sentence[-1] == "?": print(sentence)
        sentences.append(sentence)
        eos.append(sentence[len(sentence)-2:len(sentence)])
        if "." in sentence[0:-2]:
            idx = sentence[0:-2].find('.')
            print(sentence)
            print("\t", sentence[idx-2:idx+1])

# print(len(dot_sent))
# print(eos)
# for root in roots:
#     if "kabul" in root:
#         print(root)