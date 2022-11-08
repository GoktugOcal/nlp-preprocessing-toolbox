from conllu import parse_incr

data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-BOUN/tr_boun-ud-train.conllu", "r", encoding="utf-8")

i=0
for tokenlist in parse_incr(data_file):
    print(tokenlist, end="\n\n")
    i = i+1
    if i>5: break