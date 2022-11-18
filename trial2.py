data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-BOUN/tr_boun-ud-train.conllu", "r", encoding="utf-8")
text = data_file.read()

roots = set()
for line in text.split("\n"):
    if "#" not in line:
        splitted = line.split("\t")
        try: 
            if splitted[3] == 'VERB': roots.add(line)
        except: pass

for root in roots:
    if "kabul" in root:
        print(root)