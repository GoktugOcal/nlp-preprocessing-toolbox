import io
f = io.open("nlp_preprocessing_toolbox/data/suffixes.txt", mode="r", encoding="utf-8")
txt = f.read()

import json

suffix_dict = {}
for item in txt.split(";"):
    items = item.split('\t')
    suffix_dict[items[0].replace("*","").strip()] = items[-1]

print(suffix_dict)

# suffix_dict = {}
# soup = BeautifulSoup(html_text, 'html.parser')
# for link in soup.find_all('pre'):
#     for item in link.text.split("\n"):
#         items = item.split('\t')
#         suffix_dict[items[0]] = items[-1]

# print(json.dumps(suffix_dict, indent=4))