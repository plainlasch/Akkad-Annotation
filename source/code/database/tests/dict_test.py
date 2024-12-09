import json
len_1_signs = {}
with open("dictionary\lookup_dict.json", "r", encoding="utf-8") as file:
    read = json.load(file)

for translit, sign in read.items():
    if len(sign) == 1:
        len_1_signs[translit] = sign
    else:
        continue

with open("dictionary/single_signs.json", "w", encoding="utf-8") as out_file:
    json.dump(len_1_signs, out_file, ensure_ascii=False, indent=4)