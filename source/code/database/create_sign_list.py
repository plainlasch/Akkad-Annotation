import json
from helpers import list_to_txt, list_to_json

def merge_new_signs(json_file, txt_file, out_file):

    # Read the JSON file and extract the sign data directly into a set
    with open(json_file, "r", encoding="utf-8") as sign_dict:
        signs_200 = json.load(sign_dict)

    # Read the text file and directly strip newlines and add to a set
    with open(txt_file, "r", encoding="utf-8") as sign_text:
        signs_400 = {line.strip("\n")[0] for line in sign_text}

    # Extract the signs from signs_200 and add them to the set
    signs_200_set = {sign for sign in signs_200.values()}

    # Combine both sets, automatically eliminating duplicates
    total_sign_set = signs_200_set | signs_400

    # Write the combined result to a file, joining the signs with newlines
    with open(out_file, "w", encoding="utf-8") as out:
        out.write("\n".join(total_sign_set) + "\n")

def update_sign_list(single_signs, new_signs, out_file):
    # Read the JSON file and extract the sign data directly into a set
    with open(single_signs, "r", encoding="utf-8") as sign_dict:
        single_signs = json.load(sign_dict)

    # Read the text file and directly strip newlines and add to a set
    with open(new_signs, "r", encoding="utf-8") as sign_text:
        new_signs = [line.strip("\n")[0] for line in sign_text]

    unknown_signs = []
    for sign in new_signs:
        if sign not in single_signs.values():
            unknown_signs.append(sign)
    list_to_txt(unknown_signs, "dictionary\sign_lists/unknown_sings.txt")

        

if __name__ == "__main__":
    #merge_new_signs("dictionary\\sign_lists\\single_signs.json", 
                   # "dictionary\\sign_lists\\gaigutherz_akk_dict.txt", 
                   # "dictionary\\sign_lists\\all_signs.txt")
    update_sign_list(out_file="signs_600.json",
                     single_signs="dictionary\sign_lists\single_signs.json",
                     new_signs="dictionary\sign_lists/all_signs.txt")

