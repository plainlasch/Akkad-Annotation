import json



null_counts = []
with open("dictionary/nb_radical_counts.json", "r", encoding="utf-8") as file:
    corpus = json.load(file)

    for sign, counts in corpus.items():
        if all(val== 0 for val in counts.values()) == True:
            null_counts.append(sign)

with open("unrecognized_signs/nb.txt", "w", encoding="utf-8") as outfile:
    for sign in null_counts:
        outfile.write(f"{sign}\n")
