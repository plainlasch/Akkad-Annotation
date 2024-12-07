# Main script integration
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":
    from Annotater import ImageAnnotator  # Assume your main script is saved as `annotator_script.py`
    from Cunei_Converter import CuneiformConverter

    root = tk.Tk()
    annotator_app = ImageAnnotator(root, json_file="dictionary\lookup_dict.json")  # Replace with your actual CSV path
    CuneiformConverter(root, annotator_app, json_file="dictionary\lookup_dict.json", font_size=20)  # Replace with your Cuneiform dictionary CSV
    root.mainloop()