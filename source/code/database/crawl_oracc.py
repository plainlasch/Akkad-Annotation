import os
import json
from bs4 import BeautifulSoup

# Folder path where your HTML files are stored
folder_path = 'raw_data'  # Replace this with the actual folder path

# Initialize an empty dictionary to store the lookup data
lookup_dict = {}

# Iterate over all HTML files in the folder
for filename in os.listdir(folder_path):
    # Process only HTML files
    if filename.endswith(".html"):
        # Open and read the content of the HTML file
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Iterate through all <tr> elements in the HTML
        for tr in soup.find_all('tr'):
            # Extract the title from the <a> tag
            title_tag = tr.find('a')
            if title_tag and title_tag.get('title'):
                title = title_tag.get('title').strip()
                
                # Extract the cuneiform sign from the <p> tag
                cuneiform_sign_tag = tr.find('p', class_='sl-td-sign noto')
                if cuneiform_sign_tag:
                    cuneiform_sign = cuneiform_sign_tag.text.strip()

                    # Add the title and cuneiform sign to the dictionary
                    if title and cuneiform_sign:
                        lookup_dict[title] = cuneiform_sign

# Save the lookup dictionary to a JSON file
json_file_path = 'dictionary/lookup_dict.json'  # Replace this with the desired path for the JSON file

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(lookup_dict, json_file, ensure_ascii=False, indent=4)

print(f"Lookup dictionary saved to {json_file_path}")
