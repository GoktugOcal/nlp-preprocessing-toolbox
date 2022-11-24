data_file = open("nlp_preprocessing_toolbox/data/UD_Turkish-BOUN/tr_boun-ud-train.conllu", "r", encoding="utf-8")
text = data_file.read()

roots = set()
roots = {}
for line in text.split("\n"):
    if "#" not in line:
        splitted = line.split("\t")
        # print(line)

        try: 
            if splitted[3] == 'NOUN':
                if splitted[2].lower() in roots.keys():
                    roots[splitted[2].lower()] += 1
                else:
                    roots[splitted[2].lower()] = 1
                
                # if splitted[2].lower() == "ve": break

                # roots.add(splitted[2].lower())
        except: pass