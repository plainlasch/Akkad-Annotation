# Main script integration
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":
    from Annotater import ImageAnnotator  # Assume your main script is saved as `annotator_script.py`
    from Cunei_Converter import CuneiformConverter
    from install_fonts import install_fonts_from_folder

    root = tk.Tk()
    install_fonts_from_folder(font_folder="fonts")
    annotator_app = ImageAnnotator(root, json_file="dictionary\lookup_dict.json")  # Replace with your actual CSV path
    CuneiformConverter(root, annotator_app, json_file="dictionary\lookup_dict.json", font_size=20)  # Replace with your Cuneiform dictionary CSV
    root.mainloop()