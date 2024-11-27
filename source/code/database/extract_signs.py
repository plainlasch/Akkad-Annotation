import pandas as pd
import os
import re

def extract_wikipedia_tables(url, output_file_prefix="cuneiform_table"):
    """
    Extracts all tables from a Wikipedia page and saves them as CSV files.
    
    :param url: The URL of the Wikipedia page containing the tables.
    :param output_file_prefix: Prefix for the output CSV file names.
    """
    try:
        # Read all tables from the Wikipedia page
        tables = pd.read_html(url)
        print(f"Found {len(tables)} tables on the page.")

        # Save each table as a CSV file
        for i, table in enumerate(tables):
            output_file = f"{output_file_prefix}_{i+1}.csv"
            table.to_csv(f"tables/{output_file}", index=False)
            print(f"Saved table {i+1} to tables/{output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def edit_tables(path_to_tables: str, save_path: str):
    for _, _, files in os.walk(path_to_tables):
        for table in files:
            data = pd.read_csv(f"tables/{table}")
            data = data.drop(columns=['MesZL','ŠL/HA','aBZL','HethZL','Unnamed: 4', 'Unicode Name','Comments'])

            data.to_csv(f"sign_lists/{table}", index=False)


def edit_columns(data: str):
    clean_cunei = []
    df = pd.read_csv(data)
    for elem in df["Unicode code point"]:
        if not isinstance(elem, str):
            elem = str(elem)
        elem = re.sub(r"U\+[0-9A-Fa-f]+", "", elem)
        clean_cunei.append(elem)
    df["Unicode code point"] = clean_cunei
    df.to_csv(f"{data}", index=False)

def del_unwanted(data: str):
    df = pd.read_csv(data)
    unnamed = [col for col in df.columns if col.startswith("Unnamed")]
    df = df.drop(columns=unnamed)
    df.to_csv(f"{data}", index=False)

# Example usage
if __name__ == "__main__":
    #wikipedia_url = "https://en.wikipedia.org/wiki/List_of_cuneiform_signs"
    #extract_wikipedia_tables(wikipedia_url)
    #edit_tables("tables", "sign_lists")
    #edit_columns("sign_lists\cuneiform_table_1.csv")
    del_unwanted("sign_lists\cuneiform_table_7.csv")
