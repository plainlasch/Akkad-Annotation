import json

def list_to_json(list_name: str, save_path: str):
    with open(save_path, "w", encoding="utf-8") as out:
        json.dump(list_name, out, ensure_ascii=False, indent=4)

def list_to_txt(list_name: str, save_path: str):
    with open(save_path, "w", encoding="utf-8") as out:
        for item in list_name:
            out.write(f"{item}\n")