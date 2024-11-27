
import ast  # To safely evaluate the string as a Python literal (list)

def read_lists_from_file(txt_path):
    """
    Read each list from the text file as a list element.

    :param txt_path: Path to the text file.
    :return: A list of lists (each line from the file is a list).
    """

    # Open and read the file
    with open(txt_path, 'r', encoding='utf-8') as file:
        line = file.read().replace('",', '",\n')
        file.write(line)

# Example usage
if __name__ == "__main__":
    txt_path = "cuneiform_signs.txt"  # Replace with the path to your text file
